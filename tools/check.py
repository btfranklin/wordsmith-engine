"""Run the complete validation gates for both language packages."""

from __future__ import annotations

from pathlib import Path
import subprocess


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_CHECKS = (
    (REPOSITORY_ROOT / "packages" / "python", ("pdm", "run", "check")),
    (REPOSITORY_ROOT / "packages" / "typescript", ("npm", "run", "check")),
)


def main() -> None:
    """Run each package's complete check, stopping at the first failure."""
    for package_directory, command in PACKAGE_CHECKS:
        print(f"Running {' '.join(command)} in {package_directory}", flush=True)
        result = subprocess.run(command, cwd=package_directory)
        if result.returncode != 0:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
