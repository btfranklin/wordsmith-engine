# Architecture

Wordsmith Engine is one dependency-free procedural text library implemented in
Python and TypeScript. The central abstraction is a lazy `Component` that
renders synchronously through a caller-owned random source.

## Repository and package boundary

- `packages/python` owns the Python implementation, tests, examples, and
  distributable metadata.
- `packages/typescript` owns the TypeScript implementation, tests, examples,
  and distributable metadata.
- `spec` owns shared behavior and conformance data, but is never a runtime
  package dependency.
- `assets` owns canonical data. Each package contains a verified byte-identical
  runtime copy.

Neither language is canonical. Shared changes are complete only when the
contract, both implementations, tests, and documentation agree.

## Runtime layers

Each implementation follows the same dependency direction:

1. Core defines components, composition, transformations, choices, and random
   helpers.
2. Words and grammar depend on core and package-local assets.
3. Names depend on core, words where appropriate, and package-local assets.
4. Generators compose core, words, names, and other generators.
5. Specials are standalone features whose behavior does not fit a component
   family.

TypeScript keeps its concrete random generator private. Public code sees only
`RandomSource.random()`. Python continues to accept `random.Random` through its
published API.

## Random-source ownership

Components never create or retain random sources during rendering. They pass
the exact source received by a parent through every nested call. The caller
defines seed identity, derives independent named streams at orchestration
boundaries, and controls source lifetime.

Same-language replay requires unchanged package content, assets, component
structure, configuration, and call order. The project has one current random
algorithm, without version dispatch or legacy paths.

## Generator design

- Prefer declarative composition and the established choice combinators.
- Preserve construction order because draw order is observable.
- Use uniform selection for assets, enum values, and local option arrays.
- Keep domain-specific cleanup and bounded retries in small private helpers.
- Keep public components immutable and defer all random selection until render.

Python uses `one_of`, `weighted_one_of`, `either`, `maybe`, `|`, and `+`.
TypeScript uses `oneOf`, `weightedOneOf`, `either`, `maybe`, `join`, and
`concat`. These spellings share behavior, not syntax.

## Language boundary

Wordsmith is English-oriented. Its articles, determiners, title casing,
pluralization, and general datasets do not promise locale-aware grammar.
Arbitrary Unicode text and curated exotic symbols must still pass through
without code-point corruption.
