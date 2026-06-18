# Architecture

Wordsmith Engine is a small Python package for deterministic-friendly text
generation. The central abstraction is `Component`: every generator renders text
with a caller-provided `random.Random`.

## Layers

- `wordsmith.core`: framework layer. Defines `Component`, literal text,
  composition operators, decorators, and choice combinators.
- `wordsmith.words`: reusable word and grammar components. Most of these choose
  uniformly from packaged assets or small in-code lists.
- `wordsmith.names`: reusable name components and enums. This layer owns
  given-name data, surnames, alien/fantasy procedural names, and person-name
  composition.
- `wordsmith.generators`: product-facing composite generators such as titles,
  towns, ships, gangs, and fictional materials.
- `wordsmith.specials`: standalone non-domain helpers such as readable IDs and
  exotic characters.
- `wordsmith.assets`: packaged JSON data loaded through `wordsmith.util.load_json`.

## Dependency Direction

- `core` must not depend on `words`, `names`, or `generators`, except decorator
  components may import article/determiner helpers at render time for grammar.
- `words` may depend on `core` and `util`.
- `names` may depend on `core`, `util`, and assets.
- `generators` may compose `core`, `words`, `names`, and other generators.
- `specials` should stay standalone unless a helper clearly belongs in `core`.

## Generator Design

- Prefer declarative composition with `one_of`, `weighted_one_of`, `either`,
  `maybe`, `|`, and `+`.
- Use `weighted_one_of` when the distribution matters or when old manual range
  logic would hide probability.
- Use `rng.choice(...)` directly for uniform selection from an asset list, enum
  values, or local option list.
- Every render path must use the caller-provided `random.Random`; construction of
  components should not resolve random choices.
- Use private helpers for domain-specific validation or cleanup that is not
  naturally expressed with the component DSL, such as fictional material root
  sanitization.

## Public Surface

Public imports are exposed from `wordsmith.__init__`, `wordsmith.generators`,
`wordsmith.names`, `wordsmith.words`, and `wordsmith.specials`.

When adding, renaming, or removing public classes or helpers, update:

- the implementation module
- the relevant package `__init__.py`
- `src/wordsmith/__init__.py`
- examples that demonstrate the feature
- tests that cover the public behavior
- README generator lists or usage examples
