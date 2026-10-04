"""Tests for the repository-level given-name asset updater."""

from __future__ import annotations

from datetime import date
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import TextIO

import pytest


def load_updater() -> ModuleType:
    updater_path = (
        Path(__file__).resolve().parents[3] / "tools" / "update_name_assets.py"
    )
    specification = importlib.util.spec_from_file_location(
        "wordsmith_update_name_assets",
        updater_path,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_name_sorting_resolves_casefold_collisions_deterministically() -> None:
    updater = load_updater()
    bindings = [
        {"label": {"value": value}}
        for value in ["áda", "alice", "Alice", "Áda", "alice"]
    ]

    assert updater.names_from_bindings(bindings) == [
        "Alice",
        "alice",
        "Áda",
        "áda",
    ]


def test_name_sorting_is_stable_across_hash_seeds() -> None:
    updater_path = (
        Path(__file__).resolve().parents[3] / "tools" / "update_name_assets.py"
    )
    probe = """
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location("updater", sys.argv[1])
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(json.dumps(module.sorted_unique_names({"áda", "alice", "Alice", "Áda"})))
"""
    outputs = []
    for seed in ("1", "2", "8675309"):
        environment = os.environ.copy()
        environment["PYTHONHASHSEED"] = seed
        outputs.append(
            json.loads(
                subprocess.check_output(
                    [sys.executable, "-c", probe, str(updater_path)],
                    env=environment,
                    text=True,
                )
            )
        )

    assert outputs == [["Alice", "alice", "Áda", "áda"]] * len(outputs)

def test_curated_additions_are_merged_into_the_intended_gender_lists() -> None:
    updater = load_updater()
    names = {
        "english_speaking": {
            "male": ["ExistingMale"],
            "female": ["ExistingFemale"],
        }
    }

    updater.apply_curated_additions(names)

    assert "Fiachna" in names["english_speaking"]["male"]
    assert "Elissa" in names["english_speaking"]["female"]
    assert "Vesper" in names["english_speaking"]["male"]
    assert "Vesper" in names["english_speaking"]["female"]
    for values in names["english_speaking"].values():
        assert values == sorted(values, key=lambda value: (value.casefold(), value))


def test_payload_uses_an_injected_or_current_refresh_date() -> None:
    updater = load_updater()
    names = {
        "english_speaking": {"male": ["A"], "female": ["B"]},
        "ancient": {"male": ["C"], "female": ["D"]},
    }

    injected = updater.build_payload(names, refreshed_on=date(2030, 2, 3))
    assert injected["_meta"]["refreshed_on"] == "2030-02-03"

    today_before = date.today().isoformat()
    current = updater.build_payload(names)
    today_after = date.today().isoformat()
    assert current["_meta"]["refreshed_on"] in {today_before, today_after}


@pytest.mark.parametrize(
    ("group", "gender"),
    [
        (group, gender)
        for group in ("english_speaking", "latin_american", "eastern", "ancient")
        for gender in ("male", "female")
    ],
)
def test_empty_query_results_preserve_the_existing_asset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    group: str,
    gender: str,
) -> None:
    updater = load_updater()
    original = updater.ASSET_PATH.read_bytes()
    asset_path = tmp_path / "Given Names.json"
    asset_path.write_bytes(original)
    monkeypatch.setattr(updater, "ASSET_PATH", asset_path)

    def fetch_names(languages: tuple[str, ...], classes: tuple[str, ...]) -> list[str]:
        if languages == updater.GROUP_LANGUAGES[group] and classes == (
            updater.GENDER_CLASSES[gender]
        ):
            return []
        return ["Téa"]

    monkeypatch.setattr(updater, "fetch_names", fetch_names)
    with pytest.raises(ValueError, match=f"{group}\\.{gender}"):
        updater.main()
    assert asset_path.read_bytes() == original
    assert list(tmp_path.iterdir()) == [asset_path]


def test_successful_refresh_replaces_the_asset_and_preserves_permissions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    updater = load_updater()
    asset_path = tmp_path / "Given Names.json"
    asset_path.write_bytes(updater.ASSET_PATH.read_bytes())
    asset_path.chmod(0o640)
    monkeypatch.setattr(updater, "ASSET_PATH", asset_path)
    monkeypatch.setattr(updater, "fetch_names", lambda languages, classes: ["Téa"])

    updater.main()

    raw = asset_path.read_bytes()
    payload = json.loads(raw)
    assert payload["modern"]["latin_american"]["male"] == ["Téa"]
    assert payload["ancient"]["female"] == ["Téa"]
    assert "Vesper" in payload["modern"]["english_speaking"]["male"]
    assert "Téa".encode() in raw
    assert raw.endswith(b"\n")
    assert asset_path.stat().st_mode & 0o777 == 0o640
    assert list(tmp_path.iterdir()) == [asset_path]


@pytest.mark.parametrize("stage", ["write", "replace"])
def test_failed_refresh_preserves_the_asset_and_removes_the_temporary_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stage: str,
) -> None:
    updater = load_updater()
    original = updater.ASSET_PATH.read_bytes()
    asset_path = tmp_path / "Given Names.json"
    asset_path.write_bytes(original)
    monkeypatch.setattr(updater, "ASSET_PATH", asset_path)
    monkeypatch.setattr(updater, "fetch_names", lambda languages, classes: ["Téa"])

    def fail_write(payload: object, file: TextIO, **options: object) -> None:
        file.write('{"partial":')
        raise OSError("Write failed")

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError("Replace failed")

    if stage == "write":
        monkeypatch.setattr(updater.json, "dump", fail_write)
    else:
        monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(OSError, match="failed"):
        updater.main()
    assert asset_path.read_bytes() == original
    assert list(tmp_path.iterdir()) == [asset_path]
