"""Synchronize canonical assets into both self-contained language packages."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIRECTORY = REPOSITORY_ROOT / "assets"
PACKAGE_DIRECTORIES = (
    REPOSITORY_ROOT / "packages" / "python" / "src" / "wordsmith" / "assets",
    REPOSITORY_ROOT / "packages" / "typescript" / "src" / "assets",
)


def asset_files(directory: Path) -> dict[str, Path]:
    return {path.name: path for path in sorted(directory.glob("*.json"))}


def synchronize() -> None:
    canonical = asset_files(CANONICAL_DIRECTORY)
    if not canonical:
        raise RuntimeError(f"No canonical JSON assets found in {CANONICAL_DIRECTORY}")

    for destination in PACKAGE_DIRECTORIES:
        destination.mkdir(parents=True, exist_ok=True)
        for existing in asset_files(destination).values():
            if existing.name not in canonical:
                existing.unlink()
        for name, source in canonical.items():
            shutil.copyfile(source, destination / name)


def verify() -> None:
    canonical = asset_files(CANONICAL_DIRECTORY)
    if not canonical:
        raise AssertionError(
            f"No canonical JSON assets found in {CANONICAL_DIRECTORY}"
        )

    expected_names = set(canonical)
    for destination in PACKAGE_DIRECTORIES:
        packaged = asset_files(destination)
        if set(packaged) != expected_names:
            raise AssertionError(
                f"Asset names differ in {destination}: "
                f"expected {sorted(expected_names)}, found {sorted(packaged)}"
            )
        for name, source in canonical.items():
            if source.read_bytes() != packaged[name].read_bytes():
                raise AssertionError(f"Asset bytes differ for {destination / name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify package copies without changing them.",
    )
    arguments = parser.parse_args()
    if arguments.check:
        verify()
    else:
        synchronize()
        verify()


if __name__ == "__main__":
    main()
