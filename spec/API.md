# Public API Mapping

The Python and TypeScript packages are equal implementations of one behavior
with language-appropriate spelling. Python renders a component with
`component(rng)`; TypeScript uses `component.render(rng)`.

## Core

| Python | TypeScript |
| --- | --- |
| `Component.make_text` / `Component.__call__` | `Component.render` |
| `text(*parts, sep=value)` | `join(parts, value)` |
| `left + right` | `concat(left, right)` |
| `left \| right` | `join([left, right], " ")` |
| component subclass | `component(renderFunction)` |
| `one_of` | `oneOf` |
| `weighted_one_of` | `weightedOneOf` |
| `either(..., first_probability=)` | `either(..., firstProbability)` |
| `maybe(..., probability=)` | `maybe(..., { probability })` |
| — | `ws` tagged template |
| — | `seededRandom(seed)` |

Fluent transformations map directly from `snake_case` to `camelCase`:
`capitalized`, `first_upper`/`firstUpper`, `title_case`/`titleCase`,
`prefixed_by_article`/`prefixedByArticle`,
`prefixed_by_determiner`/`prefixedByDeterminer`, and
`possessive_form`/`possessiveForm`.

## Words and grammar

Both packages export `Adjective`, `Adverb`, `Article`, `AuthoredArtifact`,
`ChemicalCompoundName`, `Determiner`, `LocationAdjective`,
`MartialSocialConcept`, `NauticalShipNameColor`, `NauticalShipNameObject`,
`Noun`, `NounForm`, `PrimitiveWeapon`, `Pronoun`, `ShipNameAdjective`,
`TimeOfDay`, `UCBerkeleyEmotion`, `Verb`, `VerbTense`, and
`VillainousPersonNoun`.

TypeScript uses immutable object parameters for configured components, such as
`new Noun({ form })`, `new Pronoun({ isSingular, isThirdPerson })`, and
`new PrimitiveWeapon({ isPlural })`. Enum members use lower camel case.

## Names

Both packages export `AlienName`, `AncientGivenName`, `BinaryGender`,
`FantasyName`, `GivenName`, `GivenNameCulture`, `PersonName`, and `Surname`.
TypeScript uses object parameters, including
`new AlienName({ syllableCount, allowHyphen, allowApostrophe })`.

## Composite generators

Both packages export `AlbumTitle`, `BandName`, `CriminalGangName`,
`FictionalElementName`, `FictionalMineralName`, `HighConceptMovieTitle`,
`LiteraryTitle`, `MovieTitle`, `NauticalShipName`, `SimpleLiteraryTitle`,
`SimpleMovieTitle`, `TownName`, and `UnusualLiteraryTitle`.

## Specials

| Python | TypeScript |
| --- | --- |
| `ExoticCharacter.random_character(rng)` | `ExoticCharacter.randomCharacter(rng)` |
| `ExoticCharacter.random_character_from_set(name, rng)` | `ExoticCharacter.randomCharacterFromSet(name, rng)` |
| `ReadableUniqueIdentifier.make_identifier(rng)` | `ReadableUniqueIdentifier.makeIdentifier(rng)` |

TypeScript requires the caller-owned RNG argument. Python retains its existing
optional system-RNG convenience for backward compatibility with the published
Python API.
