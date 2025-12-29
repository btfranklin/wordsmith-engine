"""Show deterministic output when using seeded RNGs."""

from __future__ import annotations

import random

from wordsmith import Component, one_of


def build_component() -> Component:
    return "Signal" | one_of("alpha", "bravo", "charlie")


def generate_samples(component: Component, seed: int, count: int) -> list[str]:
    rng = random.Random(seed)
    return [component(rng) for _ in range(count)]


def main() -> None:
    component = build_component()
    samples_a = generate_samples(component, seed=42, count=6)
    samples_b = generate_samples(component, seed=42, count=6)

    print("Samples A:")
    for sample in samples_a:
        print(sample)

    print("\nSamples B:")
    for sample in samples_b:
        print(sample)

    print(f"\nDeterministic match: {samples_a == samples_b}")


if __name__ == "__main__":
    main()
