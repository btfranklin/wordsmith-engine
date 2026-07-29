# Wordsmith Engine Behavioral Contract

## Purpose

This directory defines behavior shared by every first-class Wordsmith Engine
implementation. Language packages own their runtime code and public ergonomics;
the files under `spec/` are test-time contract artifacts and must not become
runtime dependencies.

The contract guarantees semantic parity, not identical syntax. Python may use
operator overloads where they are idiomatic, while TypeScript may use named
combinators for the same underlying operation.

This first contract version covers the `Component` rendering model and ordered
text composition. Other existing Python behavior remains governed by the
Python package, tests, and documentation until it is added here.

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

Default random sources, seeded-generator APIs, exception classes, identifier
casing, and other language-specific ergonomics are outside this contract. The
project does not promise that the same integer seed produces identical output
across languages.

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
Functions remain separate from the minimal component interface so custom
components need only implement rendering.

Concrete class names are not part of the shared contract. In particular, a
TypeScript implementation may keep its sequence class private or choose a name
that does not conflict with the browser's global `Text` class.

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

## Change Control

A shared behavior change is incomplete until all of the following agree:

- this behavioral contract
- affected conformance fixtures
- every first-class implementation
- implementation-specific tests
- public documentation

Fixture formats carry a `schemaVersion`. A schema change must increment that
version and update every fixture consumer in the same change.
