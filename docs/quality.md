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

After installing both development environments, the repository-level gate runs
the package checks sequentially and stops at the first failure:

```bash
python tools/check.py
```

The root runner deliberately performs no installation or dependency updates.
The Python `check-core` gate runs asset validation and freshness, Ruff, strict
mypy over the complete source tree and a typed public consumer, pytest, and
every public example in a fresh interpreter. The full Python check then builds,
inspects, and installs the distribution artifacts.

The TypeScript core gate validates assets and Biome, builds `dist` once with
TypeScript 7, then checks the compiled-tree consumer, examples, Node tests, and
TypeScript 6 declaration compatibility. Standalone typecheck, test, and example
commands build first for convenience; package verification deliberately gets a
fresh build through `prepack`.

## Shared behavior

Every implementation consumes every JSON file under `spec/conformance/` in its
tests. A shared change must update the contract, fixtures, both implementations,
implementation tests, examples where relevant, and public documentation.

Generator traces use scripted fractions rather than either language's seeded
PRNG. They lock shared branch behavior and draw consumption without promising
equal cross-language output for equal seeds. Every trace has a unique name and
nonempty human-readable intent; intent documents the path without becoming an
interpreted generator recipe. The public API fixture is the machine-readable
export inventory behind `spec/API.md`.

Python's typed-consumer fixture protects the public annotations independently
of runtime tests. TypeScript examples are discovered recursively from compiled
output, run in deterministic path order, and must each produce output, so a new
example cannot silently fall outside the examples gate.

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
must prove every package-local JSON file matches the canonical bytes.

Artifact verification also rejects runtime dependency metadata. The npm
verifier separates archive selection, shape inspection, isolated installation,
runtime/declaration/browser consumers, installed assets and metadata, and final
reporting into named lifecycle stages. Fresh npm packs and recovery tarballs
pass through those same inspection stages.

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
