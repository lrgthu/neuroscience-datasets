"""Repository loader and cross-artifact integrity checker for dataset entries."""

from __future__ import annotations

import dataclasses
import hashlib
import pathlib
import re
from collections.abc import Mapping
from typing import Any

import yaml

from neuro_datasets import schema

_BIB_ENTRY_PATTERN = re.compile(
    r"@(?P<entry_type>[A-Za-z]+)\s*\{\s*(?P<key>[^,\s]+)\s*,", re.MULTILINE
)


@dataclasses.dataclass(frozen=True)
class LoadedCatalog:
    """Bundle of validated dataset records, Markdown cards, and BibTeX snippets."""

    records: tuple[schema.DatasetRecord, ...]
    cards_by_id: Mapping[str, str]
    bibtex_by_key: Mapping[str, str]
    input_sha256: str


def parse_bibtex_entries(bib_path: pathlib.Path) -> dict[str, str]:
    """Extracts raw BibTeX entry blocks keyed by citation key from a .bib file.

    Args:
        bib_path: Path to the canonical `references.bib` file.

    Returns:
        Dictionary mapping BibTeX citation keys to raw `@type{key, ...}` blocks.

    Raises:
        ValueError: If `bib_path` is missing or contains duplicate BibTeX keys.
    """
    if not bib_path.is_file():
        raise ValueError(f"Missing bibliography file: {bib_path}")
    text = bib_path.read_text(encoding="utf-8")
    matches = list(_BIB_ENTRY_PATTERN.finditer(text))
    entries: dict[str, str] = {}
    for idx, match in enumerate(matches):
        key = match.group("key").strip()
        if key in entries:
            raise ValueError(f"Duplicate BibTeX key {key!r} in {bib_path}")
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        entries[key] = text[start:end].strip()
    return entries


def _compute_inputs_sha256(paths: tuple[pathlib.Path, ...], root: pathlib.Path) -> str:
    hasher = hashlib.sha256()
    for file_path in sorted(paths):
        rel = file_path.relative_to(root).as_posix()
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(file_path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def _validate_cross_links(
    record: schema.DatasetRecord,
    yaml_path: pathlib.Path,
    repo_root: pathlib.Path,
    bibtex_by_key: Mapping[str, str],
) -> str:
    expected_parent = yaml_path.parent.name
    if expected_parent != record.category:
        raise ValueError(
            f"{yaml_path}: directory {expected_parent!r} != category {record.category!r}"
        )
    if yaml_path.stem != record.id:
        raise ValueError(
            f"{yaml_path}: filename stem {yaml_path.stem!r} != id {record.id!r}"
        )
    card_file = repo_root / record.card_path
    if not card_file.is_file():
        raise ValueError(f"{yaml_path}: missing Markdown card {card_file}")
    card_text = card_file.read_text(encoding="utf-8").strip()
    if len(card_text) < 200:
        raise ValueError(
            f"{card_file}: Markdown card is too short ({len(card_text)} chars)"
        )
    all_keys = record.citations.primary_bib_keys + record.citations.related_bib_keys
    for bib_key in all_keys:
        if bib_key not in bibtex_by_key:
            raise ValueError(
                f"{yaml_path}: undefined BibTeX key {bib_key!r} (not in references.bib)"
            )
    return card_text


def load_repository_catalog(repo_root: pathlib.Path) -> LoadedCatalog:
    """Loads and cross-validates all YAML specs, Markdown cards, and BibTeX keys.

    Args:
        repo_root: Root directory of the `neuroscience-datasets` repository.

    Returns:
        Immutable LoadedCatalog sorted deterministically by category and dataset id.

    Raises:
        ValueError: If no datasets exist, IDs collide, or cross-references fail.
    """
    datasets_dir = repo_root / "datasets"
    bib_path = repo_root / "references.bib"
    if not datasets_dir.is_dir():
        raise ValueError(f"Missing datasets directory: {datasets_dir}")
    bibtex_by_key = parse_bibtex_entries(bib_path)
    yaml_files = sorted(datasets_dir.rglob("*.yaml"))
    if not yaml_files:
        raise ValueError(f"No dataset YAML files found under {datasets_dir}")

    records_by_id: dict[str, schema.DatasetRecord] = {}
    cards_by_id: dict[str, str] = {}
    tracked_files: list[pathlib.Path] = [bib_path]

    for yaml_path in yaml_files:
        with yaml_path.open("r", encoding="utf-8") as handle:
            raw_obj: Any = yaml.safe_load(handle)
        if not isinstance(raw_obj, Mapping):
            raise ValueError(f"{yaml_path}: expected top-level YAML mapping")
        record = schema.parse_dataset_record(raw_obj, str(yaml_path))
        if record.id in records_by_id:
            raise ValueError(f"Duplicate dataset id={record.id!r} in {yaml_path}")
        card_text = _validate_cross_links(record, yaml_path, repo_root, bibtex_by_key)
        records_by_id[record.id] = record
        cards_by_id[record.id] = card_text
        tracked_files.append(yaml_path)
        tracked_files.append(repo_root / record.card_path)

    ordered_records = tuple(
        sorted(records_by_id.values(), key=lambda r: (r.category, r.id))
    )
    digest = _compute_inputs_sha256(tuple(tracked_files), repo_root)
    return LoadedCatalog(
        records=ordered_records,
        cards_by_id=cards_by_id,
        bibtex_by_key=bibtex_by_key,
        input_sha256=digest,
    )
