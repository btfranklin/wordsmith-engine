"""Generate sample movie titles."""

from __future__ import annotations

import random

from wordsmith import HighConceptMovieTitle, MovieTitle, SimpleMovieTitle


def main() -> None:
    rng = random.Random(11)

    print("Mixed movie titles:")
    for _ in range(8):
        print(MovieTitle()(rng))

    print("\nSimple movie titles:")
    for _ in range(5):
        print(SimpleMovieTitle()(rng))

    print("\nHigh-concept movie titles:")
    for _ in range(5):
        print(HighConceptMovieTitle()(rng))


if __name__ == "__main__":
    main()
