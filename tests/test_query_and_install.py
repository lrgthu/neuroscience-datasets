"""Unit and integration tests for KB query ranking and multi-agent skill installation."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

from neuro_datasets import query

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
QUERY_CLI = (
    REPO_ROOT / "skills" / "neuroscience-datasets" / "scripts" / "query_kb.py"
)
INSTALL_CLI = REPO_ROOT / "scripts" / "install_agent_skill.py"


def test_synonym_and_facet_search_against_live_catalog() -> None:
    payload = query.load_compiled_catalog(REPO_ROOT / "catalog" / "datasets.json")
    nhp_results = query.search_catalog(
        payload,
        query.SearchFilter(
            query="nhp THINGS visual",
            access_tiers=("open",),
            top_k=5,
        ),
    )
    assert nhp_results
    assert nhp_results[0].entry["id"] == "tvsd"

    connectome_results = query.search_catalog(
        payload,
        query.SearchFilter(
            query="em connectome",
            species=("drosophila",),
            top_k=5,
        ),
    )
    found_ids = {item.entry["id"] for item in connectome_results}
    assert {"flywire_connectome", "hemibrain_flyem"} <= found_ids

    it_results = query.search_catalog(
        payload,
        query.SearchFilter(query="macaque IT feedback latency", top_k=3),
    )
    assert it_results[0].entry["id"] == "kar_dicarlo_recurrent_it"


def test_exact_ids_order_and_unique_bibtex_deduplication() -> None:
    payload = query.load_compiled_catalog(REPO_ROOT / "catalog" / "datasets.json")
    selected = query.search_catalog(
        payload,
        query.SearchFilter(ids=("tvsd", "things_data", "nsd"), top_k=10),
    )
    assert [item.entry["id"] for item in selected] == ["tvsd", "things_data", "nsd"]
    bib_text = query.collect_unique_bibtex(selected)
    assert "@article{" in bib_text
    headers = [
        line.strip() for line in bib_text.splitlines() if line.strip().startswith("@")
    ]
    assert len(headers) == len(set(headers))


@pytest.mark.parametrize("bad_top_k", [0, -5, 501, True])
def test_invalid_top_k_rejected(bad_top_k: int) -> None:
    payload = query.load_compiled_catalog(REPO_ROOT / "catalog" / "datasets.json")
    with pytest.raises(ValueError, match="top_k"):
        query.search_catalog(payload, query.SearchFilter(top_k=bad_top_k))


def test_standalone_query_cli_modes() -> None:
    stats_proc = subprocess.run(
        [sys.executable, str(QUERY_CLI), "--kb-root", str(REPO_ROOT), "--stats", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    stats = json.loads(stats_proc.stdout)
    assert stats["dataset_count"] >= 112

    pit_proc = subprocess.run(
        [
            sys.executable,
            str(QUERY_CLI),
            "--kb-root",
            str(REPO_ROOT),
            "--ids",
            "zuco,open_fmind",
            "--pitfalls",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Standard Splits" in pit_proc.stdout
    assert "zuco" in pit_proc.stdout
    assert "open_fmind" in pit_proc.stdout


def test_multi_agent_installer_idempotence_and_codex_32k_guard(
    tmp_path: pathlib.Path,
) -> None:
    fake_home = tmp_path / "home"
    (fake_home / ".gemini" / "config" / "rules").mkdir(parents=True)
    (fake_home / ".claude").mkdir(parents=True)
    (fake_home / ".codex").mkdir(parents=True)

    agy_rules = fake_home / ".gemini" / "config" / "rules" / "AGENTS.md"
    agy_rules.write_text(
        "# Header\n\n<!-- scientific-research-skills:start -->\nSRS\n<!-- scientific-research-skills:end -->\n",
        encoding="utf-8",
    )
    claude_md = fake_home / ".claude" / "CLAUDE.md"
    claude_md.write_text(
        "<!-- scientific-research-skills:start -->\nSRS\n<!-- scientific-research-skills:end -->\n",
        encoding="utf-8",
    )
    # Simulate a 32,766-byte Codex AGENTS.md right at the 32 KiB default cap.
    codex_agents = fake_home / ".codex" / "AGENTS.md"
    near_cap_body = "# Codex Rules\n" + ("x" * (32_766 - len("# Codex Rules\n")))
    assert len(near_cap_body.encode("utf-8")) == 32_766
    codex_agents.write_text(near_cap_body, encoding="utf-8")

    for _ in range(2):
        subprocess.run(
            [
                sys.executable,
                str(INSTALL_CLI),
                "--repo-root",
                str(REPO_ROOT),
                "--home-dir",
                str(fake_home),
                "--targets",
                "all",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    plugin_root = fake_home / ".gemini" / "config" / "plugins" / "neuroscience-datasets"
    assert (plugin_root / "plugin.json").is_file()
    assert (plugin_root / "assets" / "logo.svg").is_file()
    assert (plugin_root / "rules" / "AGENTS.md").is_file()
    assert (
        (plugin_root / "skills" / "neuroscience-datasets" / ".kb_root")
        .read_text(encoding="utf-8")
        .strip()
        == str(REPO_ROOT.resolve())
    )
    assert agy_rules.read_text(encoding="utf-8").count("<!-- neuroscience-datasets-kb:start -->") == 1
    assert claude_md.read_text(encoding="utf-8").count("<!-- neuroscience-datasets-kb:start -->") == 1

    # Codex skill is installed while near-cap AGENTS.md is preserved byte-for-byte!
    assert (
        fake_home / ".codex" / "skills" / "neuroscience-datasets" / "SKILL.md"
    ).is_file()
    assert codex_agents.read_text(encoding="utf-8") == near_cap_body
