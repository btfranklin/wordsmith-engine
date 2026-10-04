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

The direct `Text`, `OneOf`, and `WeightedOneOf` constructors accept lists or
tuples of components and store immutable tuples. Later changes to an input
list do not change the component. The `text`, `one_of`, and `weighted_one_of`
helpers also accept strings.

Pass the same caller-owned `random.Random` through every related Wordsmith
render. Isolate that RNG from unrelated consumers when its output must be
replayable.

Custom components must depend only on that RNG and fixed captured
configuration to remain replayable. Pin the Python runtime as well as the
package when durable replay includes non-English host case conversion.

See the [repository README](https://github.com/btfranklin/wordsmith-engine) for
the complete feature list, TypeScript usage, examples, and development guide.
