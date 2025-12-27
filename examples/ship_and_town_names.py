"""Generate nautical ship names and town names."""

from __future__ import annotations

import random

from wordsmith import NauticalShipName, TownName


def main() -> None:
    rng = random.Random(11)

    print("Ship names:")
    for _ in range(10):
        print(NauticalShipName()(rng))

    print("\nTown names:")
    for _ in range(10):
        print(TownName()(rng))


if __name__ == "__main__":
    main()
