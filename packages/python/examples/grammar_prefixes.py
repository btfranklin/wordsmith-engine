"""Grammar-focused Wordsmith examples."""

from __future__ import annotations

import random

from wordsmith import Component, one_of


def build_phrases() -> list[Component]:
    noun = one_of("owl", "engine", "hour", "mountain")
    return [
        noun.prefixed_by_article(),
        noun.prefixed_by_determiner(),
        noun.possessive_form(),
        ("the" | noun | "returns").first_upper(),
    ]


def main() -> None:
    rng = random.Random(7)
    phrases = build_phrases()

    for component in phrases:
        print(component(rng))


if __name__ == "__main__":
    main()
