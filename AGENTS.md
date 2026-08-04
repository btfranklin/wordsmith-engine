# Repository Guidelines

## Repo Map

- `packages/python/`: Python source, tests, examples, manifest, and lockfile.
- `packages/typescript/`: TypeScript source, tests, examples, manifest, and lockfile.
- `assets/`: canonical JSON data. Package-local copies are generated from here.
- `spec/`: language-neutral behavior, API mapping, and conformance fixtures.
- `docs/`: architecture, asset provenance, and quality/release guidance.
- `tools/`: repository-level maintenance shared by both packages.

## Sources Of Truth

- Start with [README.md](README.md) for public usage and the feature list.
- Read [spec/BEHAVIOR.md](spec/BEHAVIOR.md) before changing shared semantics.
- Keep [spec/API.md](spec/API.md) aligned with both public package surfaces.
- Use [docs/architecture.md](docs/architecture.md) before changing boundaries.
- Use [docs/quality.md](docs/quality.md) before committing or releasing.

## Development Commands

Run Python commands from `packages/python/`:

- `pdm install --group dev`
- `pdm run check`
- `pdm run python examples/<script>.py`

Run TypeScript commands from `packages/typescript/`:

- `npm ci`
- `npm run check`
- `npm run examples`

Synchronize canonical assets from the repository root with
`python tools/sync_assets.py`; verify them with `--check`.
Refresh canonical given-name data with `python tools/update_name_assets.py`.

## Implementation Rules

- Preserve idiomatic parity: Python uses snake_case and operators; TypeScript
  uses camelCase and named composition functions.
- Update `spec/`, both implementations, tests, examples, and public docs for a
  shared behavior change.
- Pass the caller-provided random source through every render. Never create,
  restart, or retain one inside a component render.
- Edit only canonical data under `assets/`, then synchronize package copies.
- Preserve asset bytes and ordering because selection by seed observes order.
- Do not add schema versions, algorithm versions, compatibility aliases, or
  transitional package layouts without a demonstrated external requirement.

## Release Notes

- Python and TypeScript release from one `vX.Y.Z` tag at the same version.
- The tag workflow creates draft notes; publishing the reviewed GitHub Release
  runs both artifact preflights before either registry publisher.
- Do not manually publish rebuilt artifacts or publish notes ahead of the draft
  workflow.
