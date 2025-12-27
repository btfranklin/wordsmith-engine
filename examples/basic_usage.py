"""Basic usage examples for the Wordsmith DSL."""

from __future__ import annotations

import random

from wordsmith import Component, either, maybe, one_of, text


def build_title() -> Component:
    descriptor = one_of("quiet", "restless", "golden", "shattered")
    subject = either("river", "city", first_probability=0.7)
    return text("The", descriptor, subject, sep=" ").title_case()


def build_line() -> Component:
    return text("Once", maybe(" upon a time", probability=0.5), ".", sep="")


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
