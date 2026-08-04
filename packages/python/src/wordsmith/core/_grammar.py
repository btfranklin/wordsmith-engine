"""Private English grammar selection shared by core and word components."""

from __future__ import annotations

import random


_ARTICLES = ("a", "the")
_DETERMINERS = ("a", "the", "my", "your", "our", "her", "his")


def select_article(rng: random.Random, *, is_before_vowel: bool) -> str:
    """Select an article, adjusting the indefinite form for a vowel sound."""
    article = rng.choice(_ARTICLES)
    if article == "a" and is_before_vowel:
        return "an"
    return article


def select_determiner(rng: random.Random, *, is_before_vowel: bool) -> str:
    """Select a determiner, adjusting the indefinite form for a vowel sound."""
    determiner = rng.choice(_DETERMINERS)
    if determiner == "a" and is_before_vowel:
        return "an"
    return determiner
