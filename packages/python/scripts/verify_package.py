"""Inspect and install the built Python artifacts."""

from __future__ import annotations

import argparse
import email
import json
import subprocess
import tarfile
import tempfile
import venv
import zipfile
from pathlib import Path


ASSET_NAMES = {
    "Adjectives.json",
    "Adverbs.json",
    "Chemical Compound Names.json",
    "Common Surnames.json",
    "Exotic Character Sets.json",
    "Given Names.json",
    "Nouns.json",
    "Verbs.json",
}
CANONICAL_ASSETS = Path(__file__).resolve().parents[3] / "assets"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--expected-version")
    return parser.parse_args()


def only_matching(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        raise AssertionError(
            f"Expected exactly one {pattern} in {directory}, found {matches}"
        )
    return matches[0]


def wheel_version(wheel: Path) -> str:
    with zipfile.ZipFile(wheel) as archive:
        members = set(archive.namelist())
        metadata_path = next(
            path for path in members if path.endswith(".dist-info/METADATA")
        )
        metadata = email.message_from_bytes(archive.read(metadata_path))
        required_suffixes = {
            "wordsmith/__init__.py",
            "wordsmith/py.typed",
            ".dist-info/licenses/LICENSE",
            *(f"wordsmith/assets/{name}" for name in ASSET_NAMES),
        }
        for suffix in required_suffixes:
            if not any(path.endswith(suffix) for path in members):
                raise AssertionError(f"Wheel is missing {suffix}")
        for name in ASSET_NAMES:
            asset_path = next(
                path for path in members if path.endswith(f"wordsmith/assets/{name}")
            )
            if archive.read(asset_path) != (CANONICAL_ASSETS / name).read_bytes():
                raise AssertionError(f"Wheel asset bytes differ for {name}")
        if any("/tests/" in f"/{path}" or "/spec/" in f"/{path}" for path in members):
            raise AssertionError("Wheel contains test or specification files")

    version = metadata["Version"]
    if version is None:
        raise AssertionError("Wheel metadata is missing Version")
    return version


def verify_sdist(sdist: Path, version: str) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        members = {member.name for member in archive.getmembers()}

    root = f"wordsmith_engine-{version}"
    required = {
        f"{root}/LICENSE",
        f"{root}/README.md",
        f"{root}/pyproject.toml",
        f"{root}/src/wordsmith/__init__.py",
        f"{root}/src/wordsmith/py.typed",
        *(f"{root}/src/wordsmith/assets/{name}" for name in ASSET_NAMES),
    }
    missing = required - members
    if missing:
        raise AssertionError(f"Source distribution is missing {sorted(missing)}")
    with tarfile.open(sdist, "r:gz") as archive:
        for name in ASSET_NAMES:
            packaged = archive.extractfile(f"{root}/src/wordsmith/assets/{name}")
            if packaged is None or packaged.read() != (
                CANONICAL_ASSETS / name
            ).read_bytes():
                raise AssertionError(
                    f"Source distribution asset bytes differ for {name}"
                )
    if any("/tests/" in f"/{path}" or "/spec/" in f"/{path}" for path in members):
        raise AssertionError("Source distribution contains test or specification files")


def verify_isolated_install(wheel: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="wordsmith-wheel-") as directory:
        environment = Path(directory)
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / "bin" / "python"
        subprocess.run(
            [
                python,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-deps",
                wheel.resolve(),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                python,
                "-c",
                (
                    "import random; "
                    "from wordsmith import LiteraryTitle, Noun; "
                    "rng = random.Random(5343); "
                    "assert LiteraryTitle()(rng); assert Noun()(rng)"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )


def main() -> None:
    arguments = parse_arguments()
    wheel = only_matching(arguments.dist, "*.whl")
    sdist = only_matching(arguments.dist, "*.tar.gz")
    version = wheel_version(wheel)
    if arguments.expected_version is not None and version != arguments.expected_version:
        raise AssertionError(
            f"Built version {version} does not match {arguments.expected_version}"
        )
    verify_sdist(sdist, version)
    verify_isolated_install(wheel)
    print(
        json.dumps(
            {"version": version, "wheel": str(wheel), "sdist": str(sdist)},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
