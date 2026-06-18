"""Refresh grouped given-name assets from Wikidata."""

from __future__ import annotations

from collections.abc import Iterable
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ASSET_PATH = Path("src/wordsmith/assets/Given Names.json")
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = (
    "wordsmith-engine name-list refresh "
    "(https://github.com/btfranklin/wordsmith-engine)"
)

GENDER_CLASSES = {
    "male": ("Q12308941", "Q3409032"),
    "female": ("Q11879590", "Q3409032"),
}

GROUP_LANGUAGES = {
    "english_speaking": (
        "Q1860",  # English
    ),
    "latin_american": (
        "Q1321",  # Spanish
        "Q5146",  # Portuguese
    ),
    "eastern": (
        "Q5287",  # Japanese
        "Q7850",  # Chinese
        "Q9176",  # Korean
        "Q9199",  # Vietnamese
        "Q9217",  # Thai
        "Q1568",  # Hindi
        "Q11059",  # Sanskrit
        "Q13955",  # Arabic
        "Q9168",  # Persian
    ),
    "ancient": (
        "Q35497",  # Ancient Greek
        "Q397",  # Latin
        "Q50868",  # Egyptian
        "Q1982248",  # Biblical Hebrew
        "Q36790",  # Sumerian
        "Q35518",  # Akkadian
    ),
}

CURATED_GENDERED_ADDITIONS = {
    "english_speaking": {
        "male": ("Fiachna",),
        "female": (
            "Elissa",
            "Tiziana",
            "Ciara",
            "Fionuala",
            "Sylvie",
            "Moyra",
        ),
    },
}

CURATED_UNISEX_ADDITIONS = {
    "english_speaking": (
        "Adair",
        "Alva",
        "Aquilla",
        "Ardell",
        "Aris",
        "Arliss",
        "Arlyn",
        "Autry",
        "Bliss",
        "Byrd",
        "Daris",
        "Dell",
        "Emerald",
        "Garnett",
        "Golden",
        "Jule",
        "Kaoru",
        "Lake",
        "Loris",
        "Lovell",
        "Merced",
        "Neely",
        "Nieves",
        "Silver",
        "Starr",
        "Temple",
        "True",
        "Valentine",
        "Ventura",
        "Vernal",
        "Vesper",
        "Wynne",
        "Zollie",
    ),
}

DISALLOWED_LABEL_PARTS = re.compile(r"[.,:;/()[\]{}]|\\bQ\\d+\\b")


def main() -> None:
    names = {
        group: {
            gender: fetch_names(languages, classes)
            for gender, classes in GENDER_CLASSES.items()
        }
        for group, languages in GROUP_LANGUAGES.items()
    }

    apply_curated_additions(names)

    payload = {
        "_meta": {
            "source": "Wikidata Query Service",
            "source_url": "https://query.wikidata.org/",
            "license": "CC0-1.0",
            "refreshed_on": "2026-06-18",
            "notes": [
                "Names are grouped by Wikidata language of work or name.",
                "Unisex given names are intentionally included in both gender lists.",
                "English labels are used for package-friendly display output.",
                "Curated additions supplied by B.T. Franklin are included in the English-speaking group.",
            ],
        },
        "modern": {
            key: value
            for key, value in names.items()
            if key != "ancient"
        },
        "ancient": names["ancient"],
    }

    ASSET_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("modern")
    for group, genders in payload["modern"].items():
        print(
            f"  {group}: "
            f"{len(genders['male'])} male, {len(genders['female'])} female"
        )
    print(
        "ancient: "
        f"{len(payload['ancient']['male'])} male, "
        f"{len(payload['ancient']['female'])} female"
    )


def fetch_names(languages: Iterable[str], classes: Iterable[str]) -> list[str]:
    query = build_query(languages, classes)
    bindings = run_query(query)
    return sorted(
        {
            normalized
            for binding in bindings
            if (normalized := normalize_name(binding["label"]["value"]))
        },
        key=str.casefold,
    )


def build_query(languages: Iterable[str], classes: Iterable[str]) -> str:
    language_values = " ".join(f"wd:{language}" for language in languages)
    class_values = " ".join(f"wd:{class_id}" for class_id in classes)
    return f"""
SELECT DISTINCT ?label WHERE {{
  VALUES ?class {{ {class_values} }}
  VALUES ?language {{ {language_values} }}
  ?item wdt:P31 ?class ;
        wdt:P407 ?language ;
        rdfs:label ?label .
  FILTER(STRSTARTS(STR(?item), "http://www.wikidata.org/entity/Q"))
  FILTER(LANG(?label) = "en")
}}
ORDER BY ?label
LIMIT 20000
"""


def run_query(query: str) -> list[dict[str, dict[str, str]]]:
    encoded = urlencode({"query": query, "format": "json"})
    request = Request(
        f"{SPARQL_ENDPOINT}?{encoded}",
        headers={"User-Agent": USER_AGENT},
    )

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                data = json.load(response)
            return list(data["results"]["bindings"])
        except Exception as error:
            last_error = error
            time.sleep(2**attempt)

    raise RuntimeError("Wikidata query failed") from last_error


def normalize_name(value: str) -> str | None:
    name = unicodedata.normalize("NFC", value.strip())
    if len(name) < 2 or len(name) > 32:
        return None
    if DISALLOWED_LABEL_PARTS.search(name):
        return None
    if any(unicodedata.category(char).startswith("N") for char in name):
        return None
    if not any(char.islower() for char in name):
        return None
    if len(name.split()) > 1:
        return None
    return name


def apply_curated_additions(names: dict[str, dict[str, list[str]]]) -> None:
    for group, genders in CURATED_GENDERED_ADDITIONS.items():
        for gender, additions in genders.items():
            names[group][gender] = sorted(
                {*names[group][gender], *additions},
                key=str.casefold,
            )

    for group, additions in CURATED_UNISEX_ADDITIONS.items():
        for gender in ("male", "female"):
            names[group][gender] = sorted(
                {*names[group][gender], *additions},
                key=str.casefold,
            )


if __name__ == "__main__":
    main()
