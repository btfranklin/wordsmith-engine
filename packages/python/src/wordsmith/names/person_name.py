"""Generate and format person names."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from hashlib import sha256
from itertools import accumulate
import math
import random
import re
import sys
from typing import Literal

from wordsmith.core.base import Component
from wordsmith.names.gender import BinaryGender
from wordsmith.names.given_name import GivenName
from wordsmith.names.given_name_culture import GivenNameCulture
from wordsmith.names.surname import Surname
from wordsmith.util import load_json

type GivenNamePart = Literal["full", "initial"]
type PersonNameStyle = Literal["plain", "varied"]
type Select = Callable[[str, int, tuple[float, ...]], int]

_styles = load_json("Person Name Styles.json")


@dataclass(frozen=True)
class PersonNameModifiers:
    """Specify the parts before and after a name."""

    prefix: str = ""
    generation: str = ""
    credentials: Sequence[str] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.prefix, str) or not isinstance(self.generation, str):
            raise TypeError("Prefix and generation must be strings.")
        if isinstance(self.credentials, str) or any(
            not isinstance(value, str) or not value.strip()
            for value in self.credentials
        ):
            raise ValueError("Credentials must be a sequence of nonempty strings.")
        object.__setattr__(self, "credentials", tuple(self.credentials))


@dataclass(frozen=True)
class _WeightedChoices[T]:
    values: tuple[T, ...]
    boundaries: tuple[float, ...]

    @classmethod
    def compile(cls, pairs: Sequence[tuple[float, T]]) -> _WeightedChoices[T]:
        weights = [weight for weight, _ in pairs]
        if any(not math.isfinite(weight) or weight < 0 for weight in weights):
            raise ValueError("Weights must be finite and non-negative.")
        active = [(weight, value) for weight, value in pairs if weight > 0]
        boundaries = tuple(accumulate(weight for weight, _ in active))
        if not boundaries or not math.isfinite(boundaries[-1]):
            raise ValueError("Weights must have a finite positive total.")
        if boundaries[-1] <= sys.float_info.min:
            scale = max(weights)
            boundaries = tuple(accumulate(weight / scale for weight, _ in active))
        return cls(tuple(value for _, value in active), boundaries)

    def select(self, label: str, select: Select) -> T:
        return self.values[select(label, len(self.values), self.boundaries)]


def _index(fraction: float, count: int, boundaries: tuple[float, ...]) -> int:
    if not boundaries:
        return int(fraction * count)
    target = fraction * boundaries[-1]
    return next(
        (index for index, boundary in enumerate(boundaries) if target < boundary),
        count - 1,
    )


def _format_parts(parts: Sequence[GivenNamePart]) -> tuple[GivenNamePart, ...]:
    if not parts or any(part not in ("full", "initial") for part in parts):
        raise ValueError("Given name format must contain full or initial parts.")
    return tuple(parts)


_default_formats = _WeightedChoices.compile(
    [(weight, _format_parts(parts)) for weight, parts in _styles["formats"]]
)
_default_modifiers = _WeightedChoices[str].compile(_styles["modifiers"])


@dataclass(frozen=True)
class PersonName(Component):
    """Generate a person name with optional initials, titles, and suffixes."""

    gender: BinaryGender | None = None
    culture: GivenNameCulture | None = None
    style: PersonNameStyle = field(default="plain", kw_only=True)
    given_name_format: Sequence[GivenNamePart] | None = field(
        default=None, kw_only=True
    )
    initial_period: bool = field(default=True, kw_only=True)
    initial_separator: str = field(default="", kw_only=True)
    prefix: str | None = field(default=None, kw_only=True)
    generation: str | None = field(default=None, kw_only=True)
    generation_separator: str = field(default=" ", kw_only=True)
    credentials: Sequence[str] | None = field(default=None, kw_only=True)
    credential_separator: str = field(default=", ", kw_only=True)
    format_weights: Sequence[tuple[float, Sequence[GivenNamePart]]] | None = field(
        default=None, kw_only=True
    )
    modifier_weights: Sequence[tuple[float, PersonNameModifiers]] | None = field(
        default=None, kw_only=True
    )
    _formats: _WeightedChoices[tuple[GivenNamePart, ...]] | None = field(
        init=False, default=None, repr=False
    )
    _modifiers: _WeightedChoices[PersonNameModifiers] | None = field(
        init=False, default=None, repr=False
    )

    def __post_init__(self) -> None:
        if self.style not in ("plain", "varied"):
            raise ValueError("Style must be plain or varied.")
        if not isinstance(self.initial_period, bool):
            raise TypeError("Initial period must be a boolean.")
        if any(
            not isinstance(separator, str)
            for separator in (
                self.initial_separator,
                self.generation_separator,
                self.credential_separator,
            )
        ):
            raise TypeError("Separators must be strings.")
        if self.given_name_format is not None:
            object.__setattr__(
                self, "given_name_format", _format_parts(self.given_name_format)
            )
        modifiers = PersonNameModifiers(
            "" if self.prefix is None else self.prefix,
            "" if self.generation is None else self.generation,
            () if self.credentials is None else self.credentials,
        )
        if self.credentials is not None:
            object.__setattr__(self, "credentials", modifiers.credentials)
        if self.format_weights is not None:
            formats = tuple(
                (weight, _format_parts(parts)) for weight, parts in self.format_weights
            )
            object.__setattr__(self, "format_weights", formats)
            object.__setattr__(self, "_formats", _WeightedChoices.compile(formats))
        if self.modifier_weights is not None:
            choices = tuple((weight, value) for weight, value in self.modifier_weights)
            if any(not isinstance(value, PersonNameModifiers) for _, value in choices):
                raise TypeError("Modifier options must be PersonNameModifiers objects.")
            object.__setattr__(self, "modifier_weights", choices)
            object.__setattr__(self, "_modifiers", _WeightedChoices.compile(choices))

    def make_text(self, rng: random.Random) -> str:
        def select(_label: str, count: int, boundaries: tuple[float, ...]) -> int:
            if boundaries:
                return _index(rng.random(), count, boundaries)
            return rng.choice(range(count))

        return self._render(select)

    def from_hash(self, digest: str) -> str:
        """Render the name for a hexadecimal SHA-256 digest."""
        if (
            not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-fA-F]{64}", digest) is None
        ):
            raise ValueError("Expected a 64-character hexadecimal SHA-256 digest.")
        prefix = bytes.fromhex(digest) + b"\0"

        def select(label: str, count: int, boundaries: tuple[float, ...]) -> int:
            draw = sha256(prefix + label.encode("utf-8")).digest()
            fraction = int.from_bytes(draw[:4], "big") / 2**32
            return _index(fraction, count, boundaries)

        return self._render(select)

    def _render(self, select: Select) -> str:
        parts = self.given_name_format
        if parts is None:
            formats = self._formats
            if formats is None and self.style == "varied":
                formats = _default_formats
            parts = ("full",) if formats is None else formats.select("format", select)

        genders = list(BinaryGender)
        cultures = list(GivenNameCulture)
        gender = self.gender or genders[select("gender", len(genders), ())]
        culture = self.culture or cultures[select("culture", len(cultures), ())]
        names = GivenName._options[culture.value][gender.value]
        given = [
            names[select(f"given.{index}", len(names), ())]
            for index in range(len(parts))
        ]
        surnames = Surname._options
        surname = surnames[select("surname", len(surnames), ())]
        modifiers = self._select_modifiers(select)

        title = modifiers.prefix if self.prefix is None else self.prefix
        generation = (
            modifiers.generation if self.generation is None else self.generation
        )
        credentials = (
            modifiers.credentials if self.credentials is None else self.credentials
        )
        result = f"{title} " if title else ""
        previous: GivenNamePart | None = None
        for part, name in zip(parts, given, strict=True):
            if previous is not None:
                result += (
                    self.initial_separator if previous == part == "initial" else " "
                )
            if part == "initial":
                letter = next(character for character in name if character.isalpha())
                result += letter.upper() + ("." if self.initial_period else "")
            else:
                result += name
            previous = part
        result += f" {surname}"
        if generation:
            result += self.generation_separator + generation
        return result + "".join(
            self.credential_separator + item for item in credentials
        )

    def _select_modifiers(self, select: Select) -> PersonNameModifiers:
        if all(
            value is not None
            for value in (self.prefix, self.generation, self.credentials)
        ):
            return PersonNameModifiers()
        if self._modifiers is not None:
            return self._modifiers.select("modifier", select)
        if self.style == "varied":
            category = _default_modifiers.select("modifier", select)
            if category == "prefix" and self.prefix is None:
                titles = _styles["titles"]
                return PersonNameModifiers(
                    prefix=titles[select("title", len(titles), ())]
                )
            if category == "generation" and self.generation is None:
                values = _styles["generations"]
                return PersonNameModifiers(
                    generation=values[select("generation", len(values), ())]
                )
            if category == "credentials" and self.credentials is None:
                values = _styles["credentials"]
                return PersonNameModifiers(
                    credentials=(values[select("credential", len(values), ())],)
                )
        return PersonNameModifiers()
