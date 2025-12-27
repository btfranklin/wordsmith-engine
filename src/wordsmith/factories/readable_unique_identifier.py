"""Readable unique identifier generator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import random

from wordsmith.core.components import either, text
from wordsmith.words.base import Adjective, Adverb, Noun, Verb, VerbTense


def _to_base36(value: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if value == 0:
        return "0"

    result = ""
    while value > 0:
        value, remainder = divmod(value, 36)
        result = digits[remainder] + result
    return result


@dataclass(frozen=True)
class ReadableUniqueIdentifierFactory:
    """Factory for readable identifiers with a timestamp suffix."""

    @staticmethod
    def make_identifier(rng: random.Random | None = None) -> str:
        if rng is None:
            rng = random.SystemRandom()

        prefix = either(
            text(Adjective(), Noun(), sep="_"),
            text(Adverb(), Verb(tense=VerbTense.PRESENT_PERFECT), sep="_"),
        ).make_text(rng)

        reference = datetime(2001, 1, 1, tzinfo=timezone.utc)
        micros = int((datetime.now(tz=timezone.utc) - reference).total_seconds() * 1_000_000)
        suffix = _to_base36(micros)
        return f"{prefix}_{suffix}"
