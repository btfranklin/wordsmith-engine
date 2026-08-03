"""Generate sample band names."""

from __future__ import annotations

import random

from wordsmith import BandName


def main() -> None:
    rng = random.Random(5)
    component = BandName()

    for _ in range(10):
        print(component(rng))


if __name__ == "__main__":
    main()
