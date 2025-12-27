"""Generate various character names."""

from __future__ import annotations

import random

from wordsmith import AncientName, BinaryGender, GivenName, PersonName, Surname, WeirdName


def main() -> None:
    rng = random.Random(13)

    print("Given names:")
    for _ in range(5):
        print(GivenName(gender=BinaryGender.FEMALE)(rng))

    print("\nSurnames:")
    for _ in range(5):
        print(Surname()(rng))

    print("\nFull names:")
    for _ in range(5):
        print(PersonName()(rng))

    print("\nWeird names:")
    for _ in range(5):
        print(WeirdName(syllable_count=3)(rng))

    print("\nAncient names:")
    for _ in range(5):
        print(AncientName(syllable_count=4)(rng))


if __name__ == "__main__":
    main()
