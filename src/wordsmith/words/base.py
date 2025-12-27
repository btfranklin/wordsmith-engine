"""Base word types used by Wordsmith generators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import load_json


@dataclass(frozen=True)
class Adjective(Component):
    """Random adjective from the asset list."""

    _options: ClassVar[list[str]] = load_json("Adjectives.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class Adverb(Component):
    """Random adverb from the asset list."""

    _options: ClassVar[list[str]] = load_json("Adverbs.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class Noun(Component):
    """Random noun with optional pluralization."""

    is_plural: bool = False

    _options: ClassVar[list[str]] = load_json("Nouns.json")

    def make_text(self, rng: random.Random) -> str:
        value = rng.choice(self._options)

        if self.is_plural:
            if value.endswith(("ay", "ey", "iy", "oy", "uy")):
                value += "s"
            elif value.endswith("y"):
                value = f"{value[:-1]}ies"
            elif value.endswith(("x", "ss", "sh", "ch")):
                value += "es"
            elif value.endswith("ife"):
                value = f"{value[:-2]}ves"
            elif value.endswith("rf"):
                value = f"{value[:-1]}ves"
            elif value.endswith("man"):
                if value == "human":
                    value = "humans"
                else:
                    value = f"{value[:-2]}en"
            elif not value.endswith("s"):
                value += "s"

        return value


class VerbTense(Enum):
    """Verb tense indices for verb rows."""

    BASE = 0
    PAST = 1
    PAST_PARTICIPLE = 2
    PRESENT = 3
    PRESENT_PERFECT = 4


@dataclass(frozen=True)
class Verb(Component):
    """Random verb in the requested tense."""

    tense: VerbTense = VerbTense.BASE

    _options: ClassVar[list[list[str]]] = load_json("Verbs.json")

    def make_text(self, rng: random.Random) -> str:
        verb_row = rng.choice(self._options)
        return verb_row[self.tense.value]


@dataclass(frozen=True)
class Pronoun(Component):
    """Random pronoun based on person and number."""

    is_singular: bool
    is_third_person: bool

    def make_text(self, rng: random.Random) -> str:
        if self.is_third_person:
            if self.is_singular:
                return rng.choice(["he", "she", "it"])
            return "they"

        if self.is_singular:
            return rng.choice(["I", "you"])
        return rng.choice(["we", "you"])


@dataclass(frozen=True)
class ChemicalCompoundName(Component):
    """Random chemical compound name."""

    _options: ClassVar[list[str]] = load_json("Chemical Compound Names.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class LocationAdjective(Component):
    """Random location adjective."""

    _options: ClassVar[list[str]] = [
        "ancient",
        "beautiful",
        "blissful",
        "breezy",
        "charming",
        "cloudy",
        "colorful",
        "dangerous",
        "dreamy",
        "dry",
        "enchanted",
        "enchanting",
        "fertile",
        "floral",
        "foggy",
        "forgotten",
        "freezing",
        "frozen",
        "ghostly",
        "gloomy",
        "glorious",
        "grand",
        "grassy",
        "haunted",
        "hilly",
        "looming",
        "majestic",
        "misty",
        "moonshine",
        "muddy",
        "mysterious",
        "mystical",
        "peaceful",
        "quiet",
        "rainy",
        "reedy",
        "rocky",
        "sandy",
        "shady",
        "silent",
        "snowy",
        "stony",
        "stormy",
        "sunny",
        "windswept",
        "windy",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class MartialSocialConcept(Component):
    """Random martial or social concept."""

    _options: ClassVar[list[str]] = [
        "ambush",
        "anger",
        "betrayal",
        "bravery",
        "conquest",
        "courage",
        "death",
        "deception",
        "delight",
        "despair",
        "devastation",
        "discipline",
        "domination",
        "famine",
        "freedom",
        "fury",
        "glory",
        "hatred",
        "honor",
        "independence",
        "justice",
        "liberation",
        "liberty",
        "mercy",
        "murder",
        "pestilence",
        "plunder",
        "pride",
        "rage",
        "regret",
        "reprisal",
        "retribution",
        "revenge",
        "righteousness",
        "slaughter",
        "terror",
        "transgression",
        "treachery",
        "treason",
        "triumph",
        "vengeance",
        "victory",
        "wrath",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class UCBerkeleyEmotion(Component):
    """Random emotion from the UC Berkeley dataset."""

    _options: ClassVar[list[str]] = [
        "admiration",
        "adoration",
        "appreciation",
        "amusement",
        "anxiety",
        "awe",
        "awkwardness",
        "boredom",
        "calmness",
        "confusion",
        "craving",
        "disgust",
        "empathy",
        "entrancement",
        "envy",
        "excitement",
        "fear",
        "horror",
        "interest",
        "joy",
        "nostalgia",
        "romance",
        "sadness",
        "satisfaction",
        "lust",
        "sympathy",
        "triumph",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class VillainousPersonNoun(Component):
    """Random villainous person noun with optional pluralization."""

    is_plural: bool

    _options: ClassVar[list[str]] = [
        "bandit",
        "brigand",
        "bruiser",
        "buccaneer",
        "burglar",
        "charlatan",
        "corsair",
        "criminal",
        "crook",
        "deceiver",
        "delinquent",
        "demon",
        "desperado",
        "devil",
        "dodger",
        "gunman",
        "hood",
        "scoundrel",
        "sinner",
        "blackguard",
        "brute",
        "creep",
        "dog",
        "filcher",
        "good-for-nothing",
        "goon",
        "grifter",
        "hellion",
        "highwayman",
        "hijacker",
        "hoodlum",
        "hooligan",
        "imp",
        "knave",
        "libertine",
        "looter",
        "lowlife",
        "maggot",
        "malefactor",
        "marauder",
        "mischief-maker",
        "miscreant",
        "mountebank",
        "mugger",
        "murderer",
        "ne'er-do-well",
        "offender",
        "outlaw",
        "pilferer",
        "pirate",
        "profligate",
        "punk",
        "prowler",
        "plunderer",
        "racketeer",
        "rapscallion",
        "rascal",
        "ravager",
        "reprobate",
        "robber",
        "rogue",
        "rook",
        "ruffian",
        "scalawag",
        "shark",
        "swindler",
        "thief",
        "thug",
        "troublemaker",
        "wretch",
        "vagabond",
        "varlet",
        "villain",
    ]

    def make_text(self, rng: random.Random) -> str:
        text = rng.choice(self._options)

        if self.is_plural:
            if text.endswith(("ay", "ey", "iy", "oy", "uy")):
                text += "s"
            elif text.endswith("y"):
                text = f"{text[:-1]}ies"
            elif text.endswith(("x", "ss", "sh", "ch")):
                text += "es"
            elif text.endswith("ife"):
                if text == "lowlife":
                    text += "s"
                else:
                    text = f"{text[:-2]}ves"
            elif text.endswith(("rf", "ief")):
                text = f"{text[:-1]}ves"
            elif text.endswith("man"):
                text = f"{text[:-2]}en"
            elif not text.endswith("s"):
                text += "s"

        return text


@dataclass(frozen=True)
class PrimitiveWeapon(Component):
    """Random primitive weapon with optional pluralization."""

    is_plural: bool = False

    _options: ClassVar[list[str]] = [
        "sword",
        "blade",
        "mace",
        "hammer",
        "knife",
        "dagger",
        "axe",
        "halberd",
        "glaive",
        "spear",
        "lance",
        "pike",
        "bow",
        "crossbow",
    ]

    def make_text(self, rng: random.Random) -> str:
        value = rng.choice(self._options)
        if self.is_plural:
            if value.endswith("ife"):
                value = f"{value[:-2]}ves"
            else:
                value += "s"
        return value


@dataclass(frozen=True)
class NauticalShipNameObject(Component):
    """Random ship name object."""

    _options: ClassVar[list[str]] = [
        "blade",
        "breeze",
        "concubine",
        "consort",
        "crown",
        "dagger",
        "dancer",
        "demon",
        "destiny",
        "devil",
        "disciple",
        "dragon",
        "dream",
        "dryad",
        "falcon",
        "flame",
        "fox",
        "ghost",
        "gypsy",
        "harpy",
        "heart",
        "hound",
        "jewel",
        "knave",
        "knight",
        "kraken",
        "lance",
        "mage",
        "maiden",
        "nightmare",
        "nymph",
        "paladin",
        "pearl",
        "princess",
        "queen",
        "revenant",
        "rogue",
        "rose",
        "serpent",
        "shield",
        "spear",
        "spirit",
        "stallion",
        "star",
        "storm",
        "sword",
        "treasure",
        "trinity",
        "warlock",
        "wench",
        "widow",
        "witch",
        "wizard",
        "wolf",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class NauticalShipNameColor(Component):
    """Random ship name color."""

    _options: ClassVar[list[str]] = [
        "amber",
        "black",
        "blue",
        "bronze",
        "copper",
        "golden",
        "gray",
        "green",
        "ivory",
        "jade",
        "obsidian",
        "red",
        "silver",
        "white",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class ShipNameAdjective(Component):
    """Random ship name adjective."""

    _options: ClassVar[list[str]] = [
        "adamantine",
        "adventurous",
        "ancient",
        "angry",
        "beastly",
        "beautiful",
        "courageous",
        "dancing",
        "dastardly",
        "draconian",
        "elder",
        "enchanted",
        "enchanting",
        "heroic",
        "immortal",
        "indestructible",
        "invincible",
        "magnificent",
        "malicious",
        "mighty",
        "nefarious",
        "perfect",
        "pious",
        "precious",
        "priceless",
        "relentless",
        "righteous",
        "saintly",
        "sinful",
        "sinister",
        "sylvan",
        "terrible",
        "terrific",
        "unstoppable",
        "unyielding",
        "valiant",
        "vengeful",
        "virtuous",
        "wandering",
        "windward",
        "wrathful",
        "yearning",
        "youthful",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class TimeOfDay(Component):
    """Random time-of-day word."""

    _options: ClassVar[list[str]] = [
        "midnight",
        "night",
        "morning",
        "dawn",
        "sunrise",
        "daytime",
        "midday",
        "afternoon",
        "evening",
        "dusk",
        "twilight",
        "sunset",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)
