# Quality And Operations

## Local validation

From `packages/python/`:

```bash
pdm install --group dev
pdm run check
```

From `packages/typescript/`:

```bash
npm ci
npm run check
```

The Python check runs Ruff, pytest, asset freshness, package build, archive
inspection, and isolated wheel installation. The TypeScript check runs Biome,
TypeScript 7 compilation, examples, Node tests, TypeScript 6 consumer
compatibility, asset freshness, npm-pack inspection, isolated installation,
and browser bundling.

## Shared behavior

Every implementation consumes every JSON file under `spec/conformance/` in its
tests. A shared change must update the contract, fixtures, both implementations,
implementation tests, examples where relevant, and public documentation.

Do not introduce fixture schema versions or random-algorithm versions by
default. Update current consumers together.

## Assets

Only edit canonical JSON under `assets/`. Then run:

```bash
python tools/sync_assets.py
python tools/validate_assets.py
python tools/sync_assets.py --check
```

Synchronization copies raw bytes. Never sort or reserialize assets as a cleanup
step: array and object order affect seeded selection. Both package verifiers
must prove all eight package-local files match the canonical bytes.

## CI

- Python CI covers 3.12, 3.13, and 3.14, then builds and installs artifacts.
- TypeScript CI covers Node 24 and 26, TypeScript 7, a TypeScript 6 declaration
  consumer, an isolated npm install, and a browser bundle.
- Release preflight builds each exact artifact once. Neither publisher runs
  unless both packages pass, except for an explicit recovery dispatch pointing
  to a previously validated artifact run. Recovery verifies that run's workflow
  identity, tag commit, successful package preflights, versions, archive
  contents, isolated installs, assets, declarations, and browser bundle again.

## Release workflow

Versions are lockstep. For `v0.4.0` and later:

1. Confirm both manifests/artifacts resolve to the intended tag version.
2. Push the tag and let the draft-release workflow create reviewable notes.
3. Publish the reviewed GitHub Release.
4. The unified workflow validates both artifacts and uses registry Trusted
   Publishing to upload those exact files.

The workflow filename and `release` environment are part of each registry's
OIDC identity. Update the existing PyPI Trusted Publisher to
`publish-packages.yml` before release.

The npm name must exist before npm permits Trusted Publisher configuration.
Because `wordsmith-engine` is initially unclaimed, its first publication needs
an explicitly authorized authenticated bootstrap; configure OIDC for subsequent
lockstep releases. Do not add a long-lived token path to the normal workflow.

Publishing is gated but not atomic. If one registry succeeds and the other
fails, retry only the failed publisher using preserved artifacts; never rebuild
or move an existing tag.
