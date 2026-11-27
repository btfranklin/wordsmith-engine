"""Check the add-on, then install and run the release ZIP in a clean game."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import struct
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
ADDON = Path("addons/wordsmith_engine")


def godot(project, *arguments, marker=None):
    command = [os.environ.get("GODOT", "godot"), "--headless", "--path", str(project)]
    result = subprocess.run(
        [*command, *map(str, arguments)], capture_output=True, text=True, timeout=300
    )
    output = result.stdout + result.stderr
    if result.returncode or "SCRIPT ERROR:" in output or (marker and marker not in output):
        raise RuntimeError(output)
    return result.stdout


def fixture_inputs(destination):
    """Keep binary64 precision when Godot reads JSON test inputs."""
    destination.mkdir()
    for source in (ROOT / "spec/conformance").glob("*.json"):
        data = json.loads(source.read_text(), parse_float=lambda token: {
            "binary64": struct.pack("<d", float(token)).hex()
        })
        (destination / source.name).write_text(json.dumps(data, ensure_ascii=False))


def build_zip(destination, version):
    archive = destination / f"wordsmith-engine-godot-{version}.zip"
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as package:
        for path in sorted((PACKAGE / ADDON).rglob("*")):
            if path.is_file() and path.suffix in {".gd", ".uid", ".json"}:
                package.write(path, path.relative_to(PACKAGE))
        package.write(ROOT / "LICENSE", ADDON / "LICENSE")
        for name in ("name-assets", "exotic-character-assets"):
            package.write(ROOT / f"docs/{name}.md", ADDON / f"{name}.md")
        package.writestr(str(ADDON / "VERSION"), version + "\n")
    return archive


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--output", type=Path, help="Keep the verified release ZIP here.")
    parser.add_argument("--tag", help="Check the package version against this tag.")
    options = parser.parse_args()
    version = json.loads((ROOT / "packages/typescript/package.json").read_text())["version"]
    if options.tag and options.tag != f"v{version}":
        parser.error(f"Package version {version} differs from tag {options.tag}")
    subprocess.run([sys.executable, ROOT / "tools/sync_assets.py", "--check"], check=True)
    with tempfile.TemporaryDirectory(prefix="wordsmith-godot-") as temporary:
        work = Path(temporary)
        godot(PACKAGE, "--import")
        fixture_inputs(work / "fixtures")
        godot(PACKAGE, "--script", "tests/conformance.gd", "--", work / "fixtures",
              marker="Wordsmith conformance passed")
        archive = build_zip(work, version)
        game = work / "game"
        with ZipFile(archive) as package:
            package.extractall(game)
        shutil.copytree(PACKAGE / "examples", game / "examples")
        for name in ("project.godot", "export_presets.cfg"):
            shutil.copy2(PACKAGE / name, game / name)
        godot(game, "--import")
        expected = godot(game, marker="Phoenix Harbor").splitlines()
        example = next(line for line in expected if "Phoenix Harbor" in line)
        pack = work / "game.pck"
        godot(game, "--export-pack", "Linux", pack)
        isolated = work / "player"
        isolated.mkdir()
        godot(isolated, "--main-pack", pack, marker=example)
        if options.output:
            options.output.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archive, options.output / archive.name)
        print(f"Verified {archive.name} in the exported game: {example}")


if __name__ == "__main__":
    main()
