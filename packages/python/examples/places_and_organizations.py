"""Generate ten names from each place and organization generator."""

from __future__ import annotations

import random

from wordsmith import LandmarkName, OrganizationName, TavernName


def main() -> None:
    for generator_type in (TavernName, LandmarkName, OrganizationName):
        rng = random.Random(5343)
        generator = generator_type()
        print(f"{generator_type.__name__}:")
        for _ in range(10):
            print(generator(rng))
        print()


if __name__ == "__main__":
    main()
