"""Generate ten names from each artifact, spell, operation, and festival generator."""

from __future__ import annotations

import random

from wordsmith import ArtifactName, SpellName, OperationName, FestivalName


def main() -> None:
    for generator_type in (ArtifactName, SpellName, OperationName, FestivalName):
        rng = random.Random(5343)
        generator = generator_type()
        print(f"{generator_type.__name__}:")
        for _ in range(10):
            print(generator(rng))
        print()


if __name__ == "__main__":
    main()
