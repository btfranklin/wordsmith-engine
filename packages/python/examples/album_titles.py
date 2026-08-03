"""Generate sample album titles."""

from __future__ import annotations

import random

from wordsmith import AlbumTitle


def main() -> None:
    rng = random.Random(13)

    print("Album titles:")
    for _ in range(18):
        print(AlbumTitle()(rng))


if __name__ == "__main__":
    main()
