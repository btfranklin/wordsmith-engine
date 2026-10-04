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

Fluent spellings map as follows: `capitalized` to `capitalized`, `first_upper`
to `firstUpper`, `title_case` to `titleCase`, `prefixed_by_article` to
`prefixedByArticle`, `prefixed_by_determiner` to `prefixedByDeterminer`, and
`possessive_form` to `possessiveForm`.

Both title-case methods uppercase the first alphabetic code point in a word
that requires capitalization. For example, `123hello world` becomes
`123Hello World`.

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

## Names

Both packages export `AlienName`, `AncientGivenName`, `BinaryGender`,
`FantasyName`, `GivenName`, `GivenNameCulture`, `PersonName`, and `Surname`.
TypeScript additionally exports the declaration-only configuration types
`AlienNameOptions`, `AncientGivenNameOptions`, `FantasyNameOptions`,
`GivenNameOptions`, and `PersonNameOptions`.

## Composite generators

Both packages export `AlbumTitle`, `BandName`, `CriminalGangName`,
`FictionalElementName`, `FictionalMineralName`, `HighConceptMovieTitle`,
`LiteraryTitle`, `MovieTitle`, `NauticalShipName`, `SimpleLiteraryTitle`,
`SimpleMovieTitle`, `TownName`, and `UnusualLiteraryTitle`.

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
