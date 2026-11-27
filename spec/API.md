# Public API Mapping

Python and TypeScript are equal implementations with language-appropriate
spelling. Python renders a component with `Component.__call__`; TypeScript uses
`Component.render`.

## Core semantics

| Meaning | Python | TypeScript |
| --- | --- | --- |
| Component base | `Component` | `Component` |
| Custom component | `Component` subclass | `component` with a `RenderFunction` |
| Fixed text | `Literal` | `literal` |
| Empty text | `Empty` | `empty` |
| Joined sequence | `Text` / `text` | `join` |
| Concatenation | `Component.__add__` | `concat` |
| Space joining | `Component.__or__` | `join` with a space |
| Uniform choice | `OneOf` / `one_of` | `oneOf` |
| Weighted choice | `WeightedOneOf` / `weighted_one_of` | `weightedOneOf` |
| Binary choice | `Either` / `either` | `either` |
| Optional text | `Maybe` / `maybe` | `maybe` with `MaybeOptions` |
| Exact template | — | `ws` |
| Seeded source | `random.Random` | `seededRandom` with a `Seed` |

TypeScript also exports the core types `ComponentLike`, `RandomSource`, and
`WeightedOption`. Its `RandomSource.random()` method returns a finite fraction
in `[0, 1)`.

Python exposes its concrete transformation wrappers because they are part of
the established package surface: `Capitalized`, `FirstUppercased`,
`TitleCased`, `PrefixedByArticle`, `PrefixedByDeterminer`, and `PossessiveForm`.
TypeScript represents the same transformations as immutable fluent components.

Python's direct `Text`, `OneOf`, and `WeightedOneOf` constructors accept
sequences of components, including lists and tuples. They store the parts,
options, and weights as tuples. A later change to an input list does not change
the component. Use `text`, `one_of`, or `weighted_one_of` to mix strings with
components.

`WeightedOneOf`, `weighted_one_of`, and `weightedOneOf` validate weights at
construction. Each weight must be finite and non-negative. The total must be
finite and greater than zero. Invalid weights raise `ValueError` in Python or
`RangeError` in TypeScript. Zero-weight options are never selected.

Fluent spellings map as follows: `capitalized` to `capitalized`, `first_upper`
to `firstUpper`, `title_case` to `titleCase`, `prefixed_by_article` to
`prefixedByArticle`, `prefixed_by_determiner` to `prefixedByDeterminer`, and
`possessive_form` to `possessiveForm`.

Both title-case methods uppercase the first alphabetic code point in a word
that requires capitalization. For example, `123hello world` becomes
`123Hello World`. A word that starts with `Mc` followed by a letter also
capitalizes that letter: `mcdowell` becomes `McDowell`.

TypeScript `MaybeOptions` can be a class instance or an object with extra
members. Only its `probability` member controls rendering. An empty plain object
uses the default probability; components remain children.

## Words and grammar

Both packages export `Adjective`, `Adverb`, `Article`, `AuthoredArtifact`,
`ChemicalCompoundName`, `Determiner`, `LocationAdjective`,
`MartialSocialConcept`, `NauticalShipNameColor`, `NauticalShipNameObject`,
`Noun`, `NounForm`, `PrimitiveWeapon`, `Pronoun`, `ShipNameAdjective`,
`TimeOfDay`, `UCBerkeleyEmotion`, `Verb`, `VerbTense`, and
`VillainousPersonNoun`.

TypeScript uses object parameters, such as `new Noun({ form })` and
`new Pronoun({ isSingular, isThirdPerson })`. Enum values use lower camel case.

## Reusable naming components

Both packages export the components below. Each selects uniformly from its
named vocabulary and accepts no constructor arguments:

`TavernAnimal`, `TavernObject`, `BusinessAnimal`, `WildAnimal`, `BusinessColor`, `LandmarkAdjective`, `LandmarkFeature`, `Habitat`, `BodyPart`, `CreatureType`, `GuildTrade`, `BusinessTrade`, `IndustrialTrade`, `ShopType`, `CelestialObjectType`, `OrganizationSymbol`.

`GuildTrade` returns a plural trade name, such as `cartographers`. It does not
infer singular forms. `LandmarkFeature` returns a feature label, which can be
plural, such as `falls`. `Habitat` returns a modifier, such as `marsh`.

`NaturalNameRoot` requires a context. Python uses
`NaturalNameRoot(context="landmark")` or `NaturalNameRoot(context="creature")`.
TypeScript uses `new NaturalNameRoot({ context: "landmark" })` or
`new NaturalNameRoot({ context: "creature" })` and exports the declaration-only
`NaturalNameRootOptions` type. Invalid contexts fail at construction with
`ValueError` in Python or `RangeError` in TypeScript. Each context keeps its own
ordered vocabulary.

`CompoundCreatureName`, `CompoundLandmarkName`, and `HeraldicSymbol` take no
constructor arguments. The compound names use title casing. `HeraldicSymbol`
returns a lowercase animal or object from the tavern palettes, with equal
probability for each palette. `OrganizationSymbol` keeps a separate palette.

These are public components, so callers can compose and transform them with
the standard helpers. All selection occurs during rendering with the supplied
random source. See [the component recipes](../docs/naming-components.md).

`ArtifactObject`, `SpellEffect`, `MagicalConcept`, `OperationColor`, and
`Season` are also public word components in both packages. They take no
constructor arguments. `MagicalConcept` supplies the same vocabulary to
artifact and spell names. `OperationColor` has its own codename palette;
`Season` selects among spring, summer, autumn, and winter.

## Names

Both packages export `AlienName`, `AncientGivenName`, `BinaryGender`,
`FantasyName`, `GivenName`, `GivenNameCulture`, `PersonName`, and `Surname`.
TypeScript additionally exports the declaration-only configuration types
`AlienNameOptions`, `AncientGivenNameOptions`, `FantasyNameOptions`,
`GivenNameOptions`, `GivenNamePart`, `PersonNameStyle`, and
`PersonNameOptions`. Python exports `PersonNameModifiers` as a frozen data
class. TypeScript exports `PersonNameModifiers` as a type for a plain object.

### Person name options

| Python | TypeScript | Effect |
| --- | --- | --- |
| `style` | `style` | Use `plain` (default) or the built-in `varied` mix. |
| `given_name_format` | `givenNameFormat` | Set a sequence of `full` and `initial` parts. |
| `initial_period` | `initialPeriod` | Add a period after each initial. Default is true. |
| `initial_separator` | `initialSeparator` | Join adjacent initials. Default is the empty string. |
| `prefix` | `prefix` | Add a title before the given names. |
| `generation` | `generation` | Add a suffix such as `IV` after the surname. |
| `generation_separator` | `generationSeparator` | Join the surname and generation. Default is one space. |
| `credentials` | `credentials` | Add an ordered list of credentials after the surname or generation. |
| `credential_separator` | `credentialSeparator` | Insert a separator before each credential. Default is comma and space. |
| `format_weights` | `formatWeights` | Set ordered `(weight, format)` pairs. |
| `modifier_weights` | `modifierWeights` | Set ordered `(weight, modifiers)` pairs. |

Each modifier option has `prefix`, `generation`, and `credentials` fields.
Omitted fields inside a modifier option contribute no text. A top-level field
overrides the same field in the selected option. Use an empty string or empty
credential sequence to suppress that field. Each weight table applies when
supplied, including in plain style. An explicit given-name format takes
precedence over format weights.

Call `person.from_hash(digest)` in Python or
`await person.fromHash(digest)` in TypeScript for cross-language hash replay.
Supply a 64-character hexadecimal SHA-256 digest. TypeScript uses Web Crypto
in supported Node.js runtimes and in secure browser contexts.

## Composite generators

Both packages export `AlbumTitle`, `BandName`, `CriminalGangName`,
`FictionalElementName`, `FictionalMineralName`, `HighConceptMovieTitle`,
`LiteraryTitle`, `MovieTitle`, `NauticalShipName`, `SimpleLiteraryTitle`,
`SimpleMovieTitle`, `TownName`, `TavernName`, `LandmarkName`,
`OrganizationName`, `BusinessName`, `CelestialBodyName`, `CreatureName`,
`ArtifactName`, `SpellName`, `OperationName`, `FestivalName`,
and `UnusualLiteraryTitle`.

`TavernName`, `LandmarkName`, `OrganizationName`, `BusinessName`,
`CelestialBodyName`, and `CreatureName` take no constructor
arguments. Each is a component and supports the standard text transformations.

`ArtifactName`, `SpellName`, `OperationName`, and `FestivalName` take no
constructor arguments. They compose the reusable word and name components
with specialized weighted patterns, using the caller-owned random source.

## Specials

Both packages export `ExoticCharacter` and `ReadableUniqueIdentifier`.

| Python | TypeScript |
| --- | --- |
| `ExoticCharacter.random_character` | `ExoticCharacter.randomCharacter` |
| `ExoticCharacter.random_character_from_set` | `ExoticCharacter.randomCharacterFromSet` |
| `ReadableUniqueIdentifier.make_identifier` | `ReadableUniqueIdentifier.makeIdentifier` |

TypeScript requires a caller-owned RNG. Python retains its existing optional
system-RNG convenience. `ReadableUniqueIdentifier` remains time-based and is
outside seed-only replay.
