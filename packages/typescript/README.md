# Wordsmith Engine for TypeScript

Composable, deterministic-friendly procedural text generation for TypeScript
and JavaScript.

The package is dependency-free, ESM-only, browser/bundler friendly, and ships
JavaScript plus TypeScript declarations. Wordsmith is fundamentally
English-oriented while preserving arbitrary Unicode text.

## Install

```shell
npm install wordsmith-engine
```

## Generate repeatable text

```typescript
import { LiteraryTitle, seededRandom } from "wordsmith-engine";

const rng = seededRandom("world:ships:5343");
const title = new LiteraryTitle();

console.log(title.render(rng));
```

The caller creates and owns the random source, passes it through every nested
Wordsmith render, and discards it when that generation operation is complete.
Keep unrelated procedural systems on independently derived named streams.

`seededRandom` accepts strings and finite safe integers. A numeric seed is
normalized to its decimal string, so `seededRandom(5343)` and
`seededRandom("5343")` produce the same TypeScript stream. Seeded output is
repeatable within an unchanged TypeScript package, asset set, component tree,
configuration, and call order; Python and TypeScript do not promise identical
output from the same seed.

## Compose components

```typescript
import { Adjective, Noun, join, seededRandom, ws } from "wordsmith-engine";

const rng = seededRandom("example");
const subject = join([new Adjective(), new Noun()], " ").titleCase();
const sentence = ws`${subject}!`;

console.log(sentence.render(rng));
```

`join(parts, separator)` and `concat(...parts)` render children once from left
to right through the same random source. They omit exact empty strings while
preserving whitespace-only results. `ws` is a tagged-template spelling of
`concat`: it preserves template text exactly and adds no spacing or cleanup.

`ReadableUniqueIdentifier` intentionally includes the current clock and is
therefore outside the seed-only replay guarantee.

## Development

```shell
npm ci
npm run check
```

The shared behavioral contract and the Python peer live in the
[repository](https://github.com/btfranklin/wordsmith-engine).
