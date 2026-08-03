"""String utilities used by Wordsmith components."""

from __future__ import annotations

VOWELS = {"a", "e", "i", "o", "u"}


def starts_with_vowel(text: str) -> bool:
    """Return True if the first word starts with a vowel sound."""
    stripped = text.strip()
    word_chars: list[str] = []
    for char in stripped:
        if char.isalpha():
            word_chars.append(char)
        elif word_chars:
            break
    if not word_chars:
        return False

    word = "".join(word_chars).lower()
    silent_h_prefixes = ("honest", "honor", "honour", "hour", "heir", "herb")
    hard_u_prefixes = ("uni", "use", "user", "ufo", "euro", "one", "once")

    if word.startswith(silent_h_prefixes):
        return True
    if word.startswith(hard_u_prefixes):
        return False
    return word[0] in VOWELS


def first_upper(text: str) -> str:
    """Uppercase the first alphabetic character, leaving the rest untouched."""
    for index, char in enumerate(text):
        if char.isalpha():
            return f"{text[:index]}{char.upper()}{text[index + 1:]}"
    return text


def title_case(text: str) -> str:
    """Apply title casing with basic English small-word rules."""
    small_words = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "for",
        "in",
        "nor",
        "of",
        "on",
        "or",
        "per",
        "so",
        "the",
        "to",
        "up",
        "via",
        "vs",
        "with",
        "yet",
    }
    punctuation = "\"'“”‘’()[]{}.,;:!?/"

    words = text.split(" ")
    last_index = len(words) - 1
    result: list[str] = []

    for index, word in enumerate(words):
        if word == "":
            continue

        leading = ""
        trailing = ""
        core = word

        while core and core[0] in punctuation:
            leading += core[0]
            core = core[1:]
        while core and core[-1] in punctuation:
            trailing = core[-1] + trailing
            core = core[:-1]

        if not core:
            result.append(word)
            continue

        core_lower = core.lower()
        if index not in {0, last_index} and core_lower in small_words:
            core_cased = core_lower
        else:
            core_cased = core_lower.capitalize()

        result.append(f"{leading}{core_cased}{trailing}")

    return " ".join(result)
