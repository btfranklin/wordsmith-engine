"""Generate identifiers and criminal gang names."""

from __future__ import annotations

import random

from wordsmith import CriminalGangName, ReadableUniqueIdentifier


def main() -> None:
    rng = random.Random(19)

    print("Criminal gangs:")
    for _ in range(8):
        print(CriminalGangName()(rng))

    print("\nReadable identifiers:")
    for _ in range(5):
        print(ReadableUniqueIdentifier.make_identifier(rng))


if __name__ == "__main__":
    main()
