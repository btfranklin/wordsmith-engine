# The Wordsmith Engine

![Wordsmith Engine banner](https://raw.githubusercontent.com/btfranklin/wordsmith-engine/main/.github/social%20preview/wordsmith_engine_social_preview.jpg "The Wordsmith Engine")

Wordsmith Engine is a dependency-free, English-oriented procedural text
toolkit with equal Python and TypeScript implementations. It builds names,
titles, places, groups, vessels, fictional materials, and custom generators
from small lazy components.

## Install

```bash
pip install wordsmith-engine
npm install wordsmith-engine
```

Python 3.12–3.14:

```python
import random

from wordsmith import Adjective, Noun

rng = random.Random(5343)
ship_name = ("The" | Adjective() | Noun()).title_case()
print(ship_name(rng))
```

TypeScript 7 / ES2022:

```typescript
import { Adjective, Noun, join, seededRandom, ws } from "wordsmith-engine";

const rng = seededRandom(5343);
const shipName = join(["The", new Adjective(), new Noun()], " ").titleCase();
console.log(shipName.render(rng));

const callSign = ws`WS-${new Noun()}`;
console.log(callSign.render(rng));
```

## Composition

Python uses its natural operator vocabulary:

- `left | right` joins with a space.
- `left + right` concatenates without a separator.
- `text(*parts, sep=separator)` joins with a chosen separator.

TypeScript uses component-aware functions:

- `join(parts, separator)` joins rendered parts.
- `concat(...parts)` concatenates rendered parts.
- `ws` is an exact tagged-template form of `concat`; it adds no whitespace.

Both languages provide uniform and weighted choices, optional parts, English
article/determiner helpers, title casing, first-letter uppercasing, and
possessive forms. Only an exact empty result is omitted during composition;
whitespace-only text is preserved.

## Deterministic streams

Every nested render receives the same caller-owned random source. Python uses
`random.Random(seed)`; TypeScript supplies `seededRandom(seed)` for string and
safe-integer seeds. Isolate that source from unrelated random consumers and
discard it after the related Wordsmith calls finish.

Higher-level generators should derive stable named seeds for independent
Wordsmith streams. Seed identity belongs to the caller. The same seed is not
expected to produce the same text across Python and TypeScript.

Replay also depends on package content, assets, component structure, and call
order. Pin the package release when stored seeds must reproduce durable output.
`ReadableUniqueIdentifier` additionally includes the current time and is
therefore outside seed-only replay.

## Included generators

- Names: `GivenName`, `Surname`, `PersonName`, `AlienName`,
  `AncientGivenName`, `FantasyName`
- Titles: `LiteraryTitle`, `MovieTitle`, `AlbumTitle`, and their public variants
- Places and groups: `TownName`, `CriminalGangName`, `BandName`
- Vessels: `NauticalShipName`
- Materials: `FictionalElementName`, `FictionalMineralName`,
  `ChemicalCompoundName`
- Specials: `ReadableUniqueIdentifier`, `ExoticCharacter`

See [the API mapping](spec/API.md) for the complete language-to-language
surface.

## Repository layout and development

```text
packages/
  python/        Python package, tests, and examples
  typescript/    TypeScript package, tests, and examples
assets/          Canonical shared data
spec/            Shared behavior and conformance fixtures
docs/            Architecture, quality, and asset provenance
```

```bash
cd packages/python
pdm install --group dev
pdm run check

cd ../typescript
npm ci
npm run check
```

The packages release in version lockstep. Canonical behavior lives in
[spec/BEHAVIOR.md](spec/BEHAVIOR.md), with operational guidance under
[docs/](docs/README.md).
