"""Generate sample work titles."""

from __future__ import annotations

import random

from wordsmith import SimpleWorkTitle, UnusualWorkTitle, WorkTitle


def main() -> None:
    rng = random.Random(7)

    print("Mixed work titles:")
    for _ in range(8):
        print(WorkTitle()(rng))

    print("\nSimple titles:")
    for _ in range(5):
        print(SimpleWorkTitle()(rng))

    print("\nUnusual titles:")
    for _ in range(5):
        print(UnusualWorkTitle()(rng))


if __name__ == "__main__":
    main()
