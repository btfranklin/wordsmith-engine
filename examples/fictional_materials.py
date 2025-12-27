"""Generate fictional elements, minerals, and compound names."""

from __future__ import annotations

import random

from wordsmith import ChemicalCompoundName, FictionalElementName, FictionalMineralName


def main() -> None:
    rng = random.Random(17)

    print("Fictional elements:")
    for _ in range(8):
        print(FictionalElementName()(rng))

    print("\nFictional minerals:")
    for _ in range(8):
        print(FictionalMineralName()(rng))

    print("\nReal compounds:")
    for _ in range(5):
        print(ChemicalCompoundName()(rng))


if __name__ == "__main__":
    main()
