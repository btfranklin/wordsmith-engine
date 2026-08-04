"""Run every public Python example in an isolated interpreter process."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    examples = sorted((PACKAGE_ROOT / "examples").glob("*.py"))
    if not examples:
        raise RuntimeError("No Python examples were found.")

    for example in examples:
        result = subprocess.run(
            [sys.executable, example],
            cwd=PACKAGE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Example failed: {example.name}\n{result.stdout}{result.stderr}"
            )
        if not result.stdout.strip():
            raise RuntimeError(f"Example produced no output: {example.name}")

    print(f"Ran {len(examples)} Python examples.")


if __name__ == "__main__":
    main()
