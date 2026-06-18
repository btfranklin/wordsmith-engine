# Repository Guidelines

## Repo Map
- `src/wordsmith/core/`: the composable `Component` DSL, operators, and combinators.
- `src/wordsmith/words/`: asset-backed word components and grammar helpers.
- `src/wordsmith/names/`: given names, surnames, generated alien/fantasy names, and culture/gender enums.
- `src/wordsmith/generators/`: higher-level generators built from core, words, and names.
- `src/wordsmith/assets/`: packaged JSON data used at runtime.
- `examples/`: runnable usage examples for the public package surface.
- `tests/`: pytest coverage for DSL behavior, generators, names, words, and assets.
- `docs/`: repo-local system of record for architecture, assets, and quality expectations.

## Sources Of Truth
- Start with [README.md](README.md) for public usage and the exported feature list.
- Use [docs/README.md](docs/README.md) as the documentation index.
- Use [docs/architecture.md](docs/architecture.md) before changing module boundaries or adding generators.
- Use [docs/name-assets.md](docs/name-assets.md) before changing given-name data or refresh logic.
- Use [docs/quality.md](docs/quality.md) before committing, releasing, or touching public exports.

## Development Commands
- Install dev dependencies with `pdm install --group dev`.
- Run tests with `pdm run pytest`.
- Run lint with `pdm run lint`.
- Build the distributable package with `pdm build`.
- Run examples with `pdm run python examples/<script>.py`.

## Implementation Rules
- Keep the public API coherent: generator renames or additions must update `src/wordsmith/generators/__init__.py`, `src/wordsmith/__init__.py`, examples, tests, and README together.
- Prefer `one_of`, `weighted_one_of`, `either`, `maybe`, `|`, and `+` for generator composition. Use direct `rng.choice(...)` for uniform asset or enum selection.
- Pass the caller-provided `random.Random` through all rendering. Do not use module-level randomness.
- Keep packaged data in `src/wordsmith/assets/`; document source and refresh process under `docs/`.
- This is a Python package, not a Django app or service. Do not add framework guidance, runtime service assumptions, migrations, or webhook conventions unless the repo actually grows that surface.

## Release Notes
- This repo uses SCM-derived versions, tag-triggered draft release notes, and release-published trusted publishing.
- For releases, push the tag and let the existing draft-release workflow create notes for review; do not manually author and publish release notes first.
