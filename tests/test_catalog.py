"""Unit and repository-wide integrity tests for neuroscience-datasets."""

from __future__ import annotations

import copy
import csv
import io
import math
import pathlib
from typing import Any

import pytest
import yaml

from neuro_datasets import exporter
from neuro_datasets import loader
from neuro_datasets import schema

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = pathlib.Path(__file__).resolve().parent / "fixtures" / "toy_dataset.yaml"


def _load_fixture_dict() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    assert isinstance(data, dict)
    return data


def test_parse_valid_fixture() -> None:
    raw = _load_fixture_dict()
    rec = schema.parse_dataset_record(raw, "fixture")
    assert rec.id == "toy_visual_bench"
    assert rec.scale.n_subjects == 4
    assert math.isclose(rec.scale.hours_per_subject or 0.0, 12.5, rel_tol=1e-9)


@pytest.mark.parametrize("bad_hours", [float("nan"), float("inf"), -1.0, 0.0, 99999.0])
def test_nan_and_out_of_bounds_hours_rejected(bad_hours: float) -> None:
    raw = copy.deepcopy(_load_fixture_dict())
    raw["scale"]["hours_per_subject"] = bad_hours
    with pytest.raises(ValueError, match="hours_per_subject"):
        schema.parse_dataset_record(raw, "fixture")


def test_bool_masquerading_as_int_rejected() -> None:
    raw = copy.deepcopy(_load_fixture_dict())
    raw["scale"]["n_subjects"] = True
    with pytest.raises(ValueError, match="n_subjects"):
        schema.parse_dataset_record(raw, "fixture")


def test_invalid_controlled_vocabulary_rejected() -> None:
    raw = copy.deepcopy(_load_fixture_dict())
    raw["modalities"] = ["fMRI_99T_Invalid"]
    with pytest.raises(ValueError, match="modalities"):
        schema.parse_dataset_record(raw, "fixture")


def test_tidy_csv_roundtrip_and_missing_values() -> None:
    raw = copy.deepcopy(_load_fixture_dict())
    raw["scale"]["hours_per_subject"] = None
    rec = schema.parse_dataset_record(raw, "fixture")
    csv_text = exporter.render_tidy_csv([rec])
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    assert len(rows) == 1
    assert rows[0]["id"] == "toy_visual_bench"
    assert rows[0]["hours_per_subject"] == ""
    assert rows[0]["n_subjects"] == "4"


def test_live_repository_catalog_integrity_and_sync() -> None:
    catalog = loader.load_repository_catalog(REPO_ROOT)
    assert len(catalog.records) >= 20
    seen_ids = {r.id for r in catalog.records}
    assert {"nsd", "things_data", "meg_masc", "podcast_ecog", "tvsd", "ibl_brain_wide_map"} <= seen_ids

    json_path = REPO_ROOT / "catalog" / "datasets.json"
    csv_path = REPO_ROOT / "catalog" / "datasets.csv"
    pages_js = REPO_ROOT / "docs" / "catalog_data.js"
    assert json_path.read_text(encoding="utf-8") == exporter.render_datasets_json(catalog)
    assert csv_path.read_text(encoding="utf-8") == exporter.render_tidy_csv(catalog.records)
    assert pages_js.read_text(encoding="utf-8") == exporter.render_pages_js(catalog)
