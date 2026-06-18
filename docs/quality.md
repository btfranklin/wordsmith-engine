# Quality And Operations

## Local Validation

Run these before committing code changes:

```bash
pdm run pytest
pdm run lint
pdm build
```

For user-facing generator changes, also run the relevant example script under
`examples/` and inspect sample output.

## CI

GitHub Actions runs tests and lint on Python 3.12, 3.13, and 3.14 for pushes and
pull requests to `main`.

## Public API Checklist

When changing generator names, exported classes, or examples:

- update all relevant `__init__.py` exports
- update README generator lists
- update or add examples
- update tests
- run all validation commands above

This repo intentionally avoids compatibility shims for renamed APIs. Make
renames complete and direct.

## Asset Checklist

When changing packaged JSON data:

- keep assets under `src/wordsmith/assets/`
- document source, license, and refresh command in `docs/`
- ensure package build includes the asset
- add deterministic tests for any behavior that depends on the new data shape

## Release Workflow

Versions are derived from SCM tags. Release notes are drafted by the existing
tag-triggered workflow.

For a release:

1. Create and push the semantic version tag.
2. Let the draft-release workflow create notes for review.
3. Review and publish the draft release.
4. Trusted publishing uploads to PyPI from the published GitHub release.

Do not manually write and publish release notes before the workflow has a chance
to create the draft.
