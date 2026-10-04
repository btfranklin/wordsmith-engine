"""Basic usage examples for the Wordsmith DSL."""

from __future__ import annotations

import random

from wordsmith import Component, Literal, Text, either, maybe, weighted_one_of


def build_title() -> Component:
    descriptor = weighted_one_of(
        (2.0, "quiet"), (1.0, "restless"), (1.0, "golden"), (1.0, "shattered")
    )
    subject = either("river", "city", first_probability=0.7)
    return Text([Literal("The"), descriptor, subject], sep=" ").title_case()


def build_line() -> Component:
    return ("Once" | maybe("upon a time", probability=0.5)) + "."


def main() -> None:
    rng = random.Random(12)
    title = build_title()
    line = build_line()

    print("Titles:")
    for _ in range(5):
        print(f"- {title(rng)}")

    print("\nLines:")
    for _ in range(5):
        print(f"- {line(rng)}")


if __name__ == "__main__":
    main()
