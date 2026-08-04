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
