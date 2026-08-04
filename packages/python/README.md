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

Pass the same caller-owned `random.Random` through every related Wordsmith
render. Isolate that RNG from unrelated consumers when its output must be
replayable.

Custom components must depend only on that RNG and fixed captured
configuration to remain replayable. Pin the Python runtime as well as the
package when durable replay includes non-English host case conversion.

See the [repository README](https://github.com/btfranklin/wordsmith-engine) for
the complete feature list, TypeScript usage, examples, and development guide.
