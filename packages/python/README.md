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

See the [repository README](https://github.com/btfranklin/wordsmith-engine) for
the complete feature list, TypeScript usage, examples, and development guide.
