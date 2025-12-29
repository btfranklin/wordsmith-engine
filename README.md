# The Wordsmith Engine

![Wordsmith Engine banner](https://raw.githubusercontent.com/btfranklin/wordsmith-engine/main/.github/social%20preview/wordsmith_engine_social_preview.jpg "The Wordsmith Engine")

[![Build Status](https://github.com/btfranklin/wordsmith-engine/actions/workflows/python-package.yml/badge.svg)](https://github.com/btfranklin/wordsmith-engine/actions/workflows/python-package.yml) [![Supports Python versions 3.12+](https://img.shields.io/pypi/pyversions/wordsmith-engine.svg)](https://pypi.python.org/pypi/wordsmith-engine)

The Wordsmith Engine is a composable, deterministic-friendly text-generation toolkit for Python.
It started as a port of the Swift package [`Wordsmith`](https://github.com/btfranklin/wordsmith)
(by the same author) and focuses on building
rich, varied text with small, reusable components.

## What it is for
- Generating names for people, towns, ships, gangs, and creative works.
- Building simple language generators from reusable parts.
- Producing repeatable output with a seeded RNG.

## Installation
Use PDM to install dependencies for development:
```bash
pdm install --group dev
```

## Quickstart
```python
from wordsmith import WorkTitle

print(WorkTitle()())
```

## Core concepts
The Wordsmith Engine is centered around the `Component` type. Each component can render text
with a provided random number generator.

Operator DSL (preferred):
- `left | right`: Join components with a space.
- `left + right`: Join components with no separator (useful for punctuation).

Key combinators:
- `text(*parts, sep="")`: Join components with a custom separator.
- `one_of(*options)`: Pick a random option.
- `weighted_one_of((weight, option), ...)`: Weighted choice across many options.
- `either(a, b, first_probability=0.5)`: Weighted choice between two options.
- `maybe(*parts, probability=0.5)`: Optionally include text.

Common decorators on components:
- `.title_case()` for title casing (with small-word rules).
- `.capitalized()` to capitalize all words.
- `.first_upper()` for first-letter capitalization.
- `.prefixed_by_article()` / `.prefixed_by_determiner()` for grammar helpers.
- `.possessive_form()` for possessives.

## Usage examples
```python
import random

from wordsmith import Adjective, Noun, WorkTitle, either, maybe, one_of

rng = random.Random(42)

title = (
    "The"
    | maybe(Adjective())
    | one_of("Journey", "Voyage", "Chronicles")
    | "of"
    | Noun().prefixed_by_article()
).title_case()

line = ("Once" | maybe("upon a time", probability=0.5)) + "."

print(title(rng))
print(line(rng))
print(WorkTitle()(rng))
```

## Generators included
The Wordsmith Engine ships with a growing set of generators:
- Names: `GivenName`, `Surname`, `PersonName`, `WeirdName`, `AncientName`
- Locations: `TownName`
- Groups: `CriminalGangName`, `BandName`
- Vessels: `NauticalShipName`
- Works: `SimpleWorkTitle`, `UnusualWorkTitle`, `WorkTitle`
- Materials: `FictionalElementName`, `FictionalMineralName`, `ChemicalCompoundName`
- Specials: `ReadableUniqueIdentifier`, `ExoticCharacter`

## Deterministic output
All components accept a `random.Random` instance. If you want repeatable results,
pass a seeded RNG.
```python
import random
from wordsmith import WorkTitle

rng = random.Random(1234)
print(WorkTitle()(rng))
print(WorkTitle()(rng))
```

## Examples
Run any script under `examples/` with PDM, for example:
```bash
pdm run python examples/work_titles.py
```

## Development
- Install: `pdm install --group dev`
- Run tests: `pdm run pytest`
- Run lint: `pdm run lint`
