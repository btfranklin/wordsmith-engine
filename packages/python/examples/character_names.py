"""Generate various character names."""

from __future__ import annotations

import random

from wordsmith import (
    AlienName,
    AncientGivenName,
    BinaryGender,
    FantasyName,
    GivenName,
    GivenNameCulture,
    PersonName,
    Surname,
)


def main() -> None:
    rng = random.Random(13)

    print("Given names:")
    for _ in range(5):
        print(
            GivenName(
                gender=BinaryGender.FEMALE,
                culture=GivenNameCulture.LATIN_AMERICAN,
            )(rng)
        )

    print("\nSurnames:")
    for _ in range(5):
        print(Surname()(rng))

    print("\nFull names:")
    for _ in range(5):
        print(PersonName()(rng))

    print("\nAlien names:")
    for _ in range(5):
        print(AlienName(syllable_count=3)(rng))

    print("\nAncient given names:")
    for _ in range(5):
        print(AncientGivenName(gender=BinaryGender.FEMALE)(rng))

    print("\nFantasy names:")
    for _ in range(5):
        print(FantasyName(syllable_count=4)(rng))


if __name__ == "__main__":
    main()
