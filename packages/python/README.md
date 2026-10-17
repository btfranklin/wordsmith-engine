# Wordsmith Engine for Python

The Python implementation of Wordsmith Engine provides composable,
deterministic-friendly procedural text components.

```bash
pip install wordsmith-engine
```

```python
import random

from wordsmith import Adjective, Noun

rng = random.Random(5343)
ship_name = ("The" | Adjective() | Noun()).title_case()
print(ship_name(rng))
```

The `title_case()` method uppercases the first alphabetic character in each word
that requires capitalization. A prefix stays in place: `123hello world` becomes
`123Hello World`, as it does in TypeScript.
Title casing also normalizes the `Mc` prefix: `mcdowell` becomes `McDowell`,
and `mccormick` becomes `McCormick`.

The direct `Text`, `OneOf`, and `WeightedOneOf` constructors accept lists or
tuples of components and store immutable tuples. Later changes to an input
list do not change the component. The `text`, `one_of`, and `weighted_one_of`
helpers also accept strings.

`WeightedOneOf` and `weighted_one_of` require finite, non-negative weights with
a finite positive total. Invalid weights raise `ValueError` at construction.
Zero weights are allowed when the total is positive; their options are never
selected.

Pass the same caller-owned `random.Random` through every related Wordsmith
render. Isolate that RNG from unrelated consumers when its output must be
replayable.

Custom components must depend only on that RNG and fixed captured
configuration to remain replayable. Pin the Python runtime as well as the
package when durable replay includes non-English host case conversion.

`TavernName`, `LandmarkName`, and `OrganizationName` create names for inns,
natural features and ruins, and guilds, orders, and societies. Each takes no
constructor arguments and composes with the other components.

`BusinessName`, `CelestialBodyName`, and `CreatureName` use the same component
interface to create fictional company, celestial body, and creature names.
They also take no constructor arguments and use the caller-owned random source.

Reusable naming parts include `TavernAnimal`, `BusinessColor`, `BodyPart`,
`CreatureType`, and `CelestialObjectType`. `CompoundCreatureName`,
`CompoundLandmarkName`, and `HeraldicSymbol` compose smaller components.
`NaturalNameRoot` selects from a required `landmark` or `creature` context.
These components keep specialized vocabularies separate.

`ArtifactName`, `SpellName`, `OperationName`, and `FestivalName` add relics,
magic, missions, and celebrations. They reuse existing name and word
components. `ArtifactObject`, `SpellEffect`, `MagicalConcept`, `OperationColor`,
and `Season` are also available for custom compositions.

See the [repository README](https://github.com/btfranklin/wordsmith-engine) for
the complete feature list, TypeScript usage, examples, and development guide.
