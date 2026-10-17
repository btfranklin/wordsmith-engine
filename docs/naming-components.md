# Reusable Naming Components

The word components below select uniformly from existing canonical lists.
Each selection uses one draw from the caller-owned random source. Their
construction does not select or render a value. Package-local asset copies
are generated from the canonical files.

## Word components

The asset labels in this table refer to:

- Place: `assets/Place and Organization Parts.json`
- Business: `assets/Business Name Parts.json`
- Creature: `assets/Creature Name Parts.json`
- Celestial: `assets/Celestial Name Parts.json`

| Component | Algorithm and source | Example word |
| --- | --- | --- |
| `TavernAnimal` | Select from Place `animals` | fox |
| `TavernObject` | Select from Place `tavernObjects` | lantern |
| `BusinessAnimal` | Select from Business `animals` | finch |
| `WildAnimal` | Select from Creature `animals` | lynx |
| `BusinessColor` | Select from Business `colors` | copper |
| `LandmarkAdjective` | Select from Place `landmarkAdjectives` | misty |
| `LandmarkFeature` | Select from Place `landmarkFeatures` | pass |
| `Habitat` | Select from Creature `habitats` | marsh |
| `BodyPart` | Select from Creature `bodyParts` | horn |
| `CreatureType` | Select from Creature `creatureTypes` | burrower |
| `GuildTrade` | Select from Place `tradesPlural` | cartographers |
| `BusinessTrade` | Select from Business `trades` | books |
| `IndustrialTrade` | Select from Business `industrialTrades` | Foundry |
| `ShopType` | Select from Business `shopTypes` | bookshop |
| `CelestialObjectType` | Select from Celestial `celestialObjects` | moon |
| `OrganizationSymbol` | Select from Place `organizationSymbols` | quill |
| `NaturalNameRoot(context="landmark")` | Select from Place `landmarkRoots` | thorn |
| `NaturalNameRoot(context="creature")` | Select from Creature `appearanceRoots` | shadow |

`GuildTrade` already returns a plural word. `LandmarkFeature` returns a label;
some labels, such as `falls` and `ruins`, are plural. `Habitat` returns a word
or phrase suitable for use as a modifier. These components do not perform
singular-to-plural conversion.

## Composed components

These Python recipes describe the implementation. `+` concatenates without a
space; `|` joins with a space. `one_of` selects uniformly. Selection remains
lazy until the component is rendered.

```python
# CompoundCreatureName: two draws.
(NaturalNameRoot(context="creature") + BodyPart()).title_case()

# CompoundLandmarkName: two draws.
(NaturalNameRoot(context="landmark") + one_of(*landmark_suffixes)).title_case()

# HeraldicSymbol: one draw for the palette, then one for its word.
one_of(TavernAnimal(), TavernObject())
```

`landmark_suffixes` is the existing Place `landmarkSuffixes` list. It remains
private to the compound recipe. `HeraldicSymbol` preserves lowercase words.
It uses the tavern palettes; it does not broaden `OrganizationSymbol`.

TypeScript uses the same structure with `concat`, `join`, `oneOf`, and
`.titleCase()`. Natural roots use an options object, such as
`new NaturalNameRoot({ context: "creature" })`.

## Parent generator recipes

The table shows one branch from each refactored generator. The complete
weighted patterns remain in [the behavioral contract](../spec/BEHAVIOR.md).

| Parent | Example Python recipe |
| --- | --- |
| `TavernName` | `("The" \| tavern_adjective \| HeraldicSymbol()).title_case()` |
| `LandmarkName` | `(LandmarkAdjective() \| LandmarkFeature()).title_case()` |
| `OrganizationName` | `(TownName() \| GuildTrade().possessive_form() \| "Guild").title_case()` |
| `BusinessName` | `(BusinessColor() \| BusinessAnimal() \| BusinessTrade()).title_case()` |
| `CelestialBodyName` | `(Surname().possessive_form() \| CelestialObjectType()).title_case()` |
| `CreatureName` | `(CompoundCreatureName() \| CreatureType()).title_case()` |

`tavern_adjective` denotes a lazy choice from the original Place
`tavernAdjectives` list. It remains a private detail of that naming style.
Landmark names also use `CompoundLandmarkName`. Creature names reuse
`CompoundCreatureName` both alone and before a creature type.

## Specialization and quality

The refactor preserves all asset bytes, list order, pattern weights, and
random draw order. `NauticalShipNameColor` and `LocationAdjective` are unchanged.
Similar words do not make two naming palettes interchangeable.

Changing a shared component affects each parent that uses it. For example,
changing `BodyPart` affects both compound-creature branches. Changing the
business animal palette does not affect taverns or wildlife.

The generators still make independent word choices. They do not check
anatomical plausibility or natural habitat. Names such as `Singing Basilisk`
and `Silent Volcano Crow` remain possible. The refactor preserves that
creative behavior; it does not add semantic filters.

## Refactor verification

The before-and-after comparison used seed `20261017` and 1,000 consecutive
outputs from each of the 19 existing generators in each language. All 38,000
outputs matched exactly. The next random-source value also matched for each
stream. The comparison checks each language against its own earlier output;
it does not compare Python seeds with TypeScript seeds.

Shared trace tests cover each new vocabulary's first and last entry, both
natural-root contexts, and the composed components. A focused test replaces
`BodyPart` during the test and confirms that the change reaches both branches
of `CreatureName` through `CompoundCreatureName`.

Sample review found no new quality loss. Existing unusual combinations include
`Ironfin Troll` and `Gloomwool Serpent`; both were present before the refactor.
