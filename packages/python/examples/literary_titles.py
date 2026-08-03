"""Generate sample literary titles."""

from __future__ import annotations

import random

from wordsmith import SimpleLiteraryTitle, UnusualLiteraryTitle, LiteraryTitle


def main() -> None:
    rng = random.Random(7)

    print("Mixed literary titles:")
    for _ in range(8):
        print(LiteraryTitle()(rng))

    print("\nSimple titles:")
    for _ in range(5):
        print(SimpleLiteraryTitle()(rng))

    print("\nUnusual titles:")
    for _ in range(5):
        print(UnusualLiteraryTitle()(rng))


if __name__ == "__main__":
    main()
