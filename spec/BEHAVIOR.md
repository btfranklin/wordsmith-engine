# Wordsmith Engine Behavioral Contract

## Purpose

This directory defines behavior shared by every first-class Wordsmith Engine
implementation. Language packages own their runtime code and public ergonomics;
the files under `spec/` are test-time contract artifacts and must not become
runtime dependencies.

The contract guarantees semantic parity, not identical syntax. Python may use
operator overloads where they are idiomatic, while TypeScript may use named
combinators for the same underlying operation.

This contract covers the `Component` rendering model, ordered text composition,
random-source ownership, shared assets, English text helpers, and the semantic
parity expected of the public generator surface. Exact public spellings are
recorded in `API.md`.

## Component Model

A component is a lazily rendered text value.

- Constructing or composing components does not render children or consume
  randomness.
- Rendering receives one caller-owned random source. A composite passes that
  same source to its children.
- Components render to strings.
- A string accepted where a component is expected represents a literal
  component with exactly that value.
- Implementations reject unsupported component-like values rather than
  coercing them through generic string conversion.
- Implementations preserve component order and snapshot the ordered collection
  supplied at construction. Later mutation of the caller's collection does not
  alter the composition.

Default random sources, exception classes, identifier casing, and other
language-specific ergonomics are outside this contract. The project does not
promise that the same seed produces identical output across languages.

## Random Source Ownership

Every component renders with a caller-owned random source. The same source is
passed explicitly through every nested Wordsmith call; components never create
or restart a source while rendering.

Python callers use `random.Random(seed)`. The TypeScript package provides
`seededRandom(seed)` because JavaScript has no standard seeded random source.
The concrete TypeScript implementation remains private behind the public random
source interface.

TypeScript seeds are strings or finite safe integers. An integer is normalized
to its decimal string, so `5343` and `"5343"` create the same stream. String
seeds are otherwise preserved exactly, without trimming, case folding, or
Unicode normalization. Fractional, non-finite, and unsafe numeric seeds are
rejected.

A TypeScript `RandomSource.random()` implementation returns a finite number in
the half-open interval `[0, 1)`. Choice and probability operations validate that
domain before using a draw. Probability checks consume one draw even at the
exact probabilities zero and one, because draw order is replay-observable.

The caller owns each source's scope and lifetime. A source intended for one
Wordsmith stream must remain isolated from unrelated random consumers, and the
caller discards it after the related Wordsmith calls finish. Wordsmith does not
retain a source after a synchronous render call returns.

There is one rendering protocol at every level: components receive a random
source. The API does not add a separate seed-taking `generate` method or a
scoped callback mechanism. Higher-level systems create independent named
streams by deriving stable seeds at their own call boundaries, then constructing
one Wordsmith source for each stream.

Within one language implementation, the same seeded source, package content,
component tree, configuration, assets, and call order produce exactly the same
output at any nesting depth. Durable replay across upgrades requires callers to
pin the package release; the project does not keep parallel versioned random
algorithms.

The built-in guarantee assumes that custom render callbacks are pure with
respect to the supplied random source and fixed captured configuration. A
callback that reads a clock, mutable external state, or another random source
defines its own nondeterminism. Host runtimes also own non-English Unicode case
mappings, so durable replay that transforms non-English text requires pinning
the Python or Node.js runtime in addition to the package.

## Shared Assets

Canonical word, name, and character data belongs in a neutral top-level asset
directory rather than inside either language implementation. Neither language
package is authoritative for shared data.

Each published package includes its own package-local copy so it remains
self-contained at runtime. Build and validation tooling must copy from the
neutral source and verify content and ordering. Ordering is observable behavior
for seeded selection and must not change accidentally during copying.

The canonical files live under the repository's top-level `assets/` directory.
Synchronization copies their bytes without parsing, sorting, or reformatting.

## Language Boundary

Wordsmith is fundamentally an English-oriented procedural text engine. Its
grammar, article selection, title casing, word data, and general-purpose
generators target English.

Implementations must preserve arbitrary Unicode text without splitting or
corrupting characters. That safety requirement does not create a promise of
multilingual grammar or locale-aware language processing. Non-English scripts
and symbols are decorative or belong to explicitly narrow features such as
exotic-character selection; those features return their selected strings
unchanged.

## Ordered Text Composition

The canonical composition operation is an ordered sequence of components with
a literal string separator.

Rendering a sequence performs these steps:

1. Render every child exactly once, from left to right, using the same random
   source received by the sequence.
2. Remove child results equal to the empty string `""`.
3. Preserve every other result exactly, including whitespace-only strings.
4. Insert the separator between the remaining results.

Consequences:

- A sequence with no remaining results renders `""`.
- A sequence with one remaining result renders that result without a separator.
- The separator is never rendered as a component and consumes no randomness.
- Empty children at the beginning, middle, or end never create leading,
  doubled, or trailing separators.
- Nested sequences retain their own separators and follow the same rendering
  rules.
- Child failures propagate immediately. The sequence does not retry a failed
  child or render later children after failure.
- Implementations may optimize composition only when the observable rendering,
  validation, child order, and random-source consumption remain unchanged.

The separator is required by the language-neutral operation. Language APIs may
provide named convenience operations with a fixed separator.

## Language API Mapping

The public spelling of ordered composition is language-specific:

| Semantic operation | Python | TypeScript peer |
| --- | --- | --- |
| Sequence with a separator | `text(*parts, sep=separator)` | `join(parts, separator)` |
| Sequence without a separator | `left + right` or `text(*parts)` | `concat(...parts)` |
| Sequence separated by spaces | `left \| right` | `join(parts, " ")` |

`concat` is exactly ordered composition with `separator = ""`; it does not
define a second rendering algorithm.

The TypeScript `join` separator is required. It does not inherit
`Array.prototype.join()`'s default comma or its generic value coercion.

TypeScript components are immutable fluent objects. They render through
`.render(rng)` and expose camelCase transformations corresponding to Python's
component methods, including `.titleCase()`, `.firstUpper()`,
`.prefixedByArticle()`, and `.possessiveForm()`. The package provides
`component(renderFunction)` for custom behavior so callers do not need to
subclass an internal base class or manually reproduce the fluent surface.

The TypeScript `ws` tagged template alternates its cooked literal segments and
component-like interpolations through `concat`. It preserves authored spaces,
punctuation, newlines, and indentation exactly. It never trims, dedents,
normalizes, or inserts whitespace.

Concrete class names are not part of the shared contract. In particular, a
TypeScript implementation may keep its sequence class private or choose a name
that does not conflict with the browser's global `Text` class.

## English Text Transformations

The fluent transformation methods are semantic peers across languages:

- `capitalized` uses the host language's word-title behavior matching the
  conformance fixture.
- `firstUpper` uppercases the first Unicode alphabetic code point and leaves
  the rest untouched; an uppercase mapping may expand to multiple code points.
- `titleCase` implements Wordsmith's fixed English small-word and punctuation
  rules and collapses empty fields created by repeated ASCII spaces.
- `prefixedByArticle` and `prefixedByDeterminer` use the documented English
  vowel-sound exceptions.
- `possessiveForm` appends only an apostrophe to text ending in lowercase `s`;
  all other text receives apostrophe-plus-`s`.

`string-transforms.json` provides exact cases for these rules and for vowel
sound detection.

These are English-oriented transformations. Exact cross-language casing is
required for the shared conformance cases and English text, while other Unicode
characters use each host language's current case mappings and may differ. Both
implementations must still return well-formed Unicode without splitting input
code points accidentally.

## Public Generator Parity

Every public Python word, name, composite generator, enum, and special has an
idiomatic TypeScript peer listed in `API.md`. Parity means equivalent inputs,
validation, source data, weights, branch construction order, retry limits, and
output domain. It does not require equal cross-language draws or output for the
same seed.

`ReadableUniqueIdentifier` is intentionally outside seed-only replay because
its suffix incorporates current UTC time. Both implementations preserve its
readable prefix and uppercase base-36 time-suffix shape.

## Conformance Fixtures

Machine-readable cases live under `spec/conformance/`. Every implementation
must consume every fixture file in its tests.

`component-sequences.json` uses these test-only part forms:

- A JSON string represents a literal component.
- `{"kind": "empty"}` represents a component that renders `""`.
- `{"kind": "sequence", ...}` represents a nested ordered sequence.
- `{"kind": "probe", ...}` represents a component that records its render,
  consumes exactly one random draw, and returns its declared text.

Probe nodes are conformance-test instrumentation, not public runtime
components. They verify laziness, single evaluation, left-to-right evaluation,
and random-source forwarding.

`generator-traces.json` uses a shared scripted stream of fractions to verify
public generator outputs, draw counts, branch boundaries, and retry behavior.
It does not use either language's seeded PRNG and therefore does not create a
cross-language seed guarantee.

`public-api.json` is the machine-readable inventory of runtime exports,
TypeScript declaration-only exports, and semantic language mappings. `API.md`
is its human-readable companion.

## Change Control

A shared behavior change is incomplete until all of the following agree:

- this behavioral contract
- affected conformance fixtures
- every first-class implementation
- implementation-specific tests
- public documentation

Change fixture formats directly and update every fixture consumer in the same
change. Add a version only when a concrete external compatibility boundary
requires one.
