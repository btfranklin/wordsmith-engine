"""Generate exotic characters from the factory."""

from __future__ import annotations

import random

from wordsmith import ExoticCharacterFactory


def main() -> None:
    rng = random.Random(23)

    print("Random characters from any set:")
    for _ in range(12):
        print(ExoticCharacterFactory.random_character(rng), end=" ")
    print()

    print("\nRunic characters:")
    for _ in range(12):
        print(ExoticCharacterFactory.random_character_from_set("runic", rng), end=" ")
    print()


if __name__ == "__main__":
    main()
