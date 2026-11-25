"""Installs and syncs the Neuroscience Datasets KB plugin/skill across AI research agents."""

from __future__ import annotations

import argparse
import dataclasses
import logging
import pathlib
import re
import shutil
import stat
from collections.abc import Sequence

logger = logging.getLogger(__name__)

ALLOWED_TARGETS: frozenset[str] = frozenset({"antigravity", "claude", "codex"})
MARKER_START = "<!-- neuroscience-datasets-kb:start -->"
MARKER_END = "<!-- neuroscience-datasets-kb:end -->"
SRS_END_MARKER = "<!-- scientific-research-skills:end -->"
ANTIGRAVITY_RULE_MAX_BYTES = 24_000
DEFAULT_CODEX_DOC_MAX_BYTES = 32_768


@dataclasses.dataclass(frozen=True)
class InstallOptions:
    """Configuration for installing the KB plugin/skill into local agent directories."""

    repo_root: pathlib.Path
    home_dir: pathlib.Path
    targets: tuple[str, ...]
    dry_run: bool = False


def _render_antigravity_overlay_block() -> str:
    return "\n".join(
        [
            MARKER_START,
            "### Domain Knowledge Base Overlay (`neuroscience-datasets`)",
            "",
            "- **Neuroscience / Brain / NeuroAI Auto-Activation (`GATE N`)**: Whenever any research session, `/plan`, `/boost`, `/grill-me`, `/goal`, `/teamwork`, subagent, workflow, or swarm explores **neuroscience, brain encoding/decoding, cross-species/cross-modal neural alignment, population dynamics, BCI, neuroimaging cohorts, or connectomics** across Stages `0 → 1 → 2 → 3`, activate `neuroscience-datasets` (`~/.gemini/config/plugins/neuroscience-datasets/skills/neuroscience-datasets/SKILL.md`) first via `query_kb.py` to lock verified sample sizes, canonical holdout splits, confound/leakage guards, local mirrors, BibTeX citations, and verified auto-backfill.",
            MARKER_END,
        ]
    )


def _render_standalone_rule_block(skill_md_display_path: str) -> str:
    return "\n".join(
        [
            MARKER_START,
            "## Neuroscience Datasets Knowledge Base Protocol (`neuroscience-datasets`)",
            "",
            f"- **GATE N — Neuroscience, NeuroAI, BCI, & Connectomics Auto-Activation** *(Non-Neuroscience & Ops Exempt)*: Whenever any research conversation, `/plan`, subagent, or workflow explores **neuroscience, brain encoding/decoding, cross-species or cross-modal neural alignment, neural population manifolds, BCI/neuroprosthetics, neuroimaging cohorts, or connectomics** across Stages `0 → 1 → 2 → 3`, you **MUST** read `{skill_md_display_path}` and run its `scripts/query_kb.py` **before** selecting datasets from memory, locking splits, writing dataloaders, or citing dataset papers.",
            "- **Confound & Pretraining-Overlap Guard**: Enforce KB-documented canonical splits (`NSD shared1000`, `UT-Speech wheretheressmoke`, `TVSD` 30-repeat test, `FALCON` held-out days), exclude `Open-fMIND`/`TUEG` upstream overlap on downstream benchmarks, and reject `Spampinato` block-confounded or `ZuCo` teacher-forced setups.",
            "- **Verified Auto-Backfill Authorized**: When exploration uncovers a high-value public neuroscience dataset or newly verified pitfall missing from `query_kb.py`, add/update it in the local `neuroscience-datasets` repository after passing `scholarly_graph.py bib-verify`, `uv run python scripts/build_catalog.py`, `uv run ruff check src scripts tests skills`, `uv run pytest -v`, and `uv run python scripts/build_catalog.py --check`, then commit locally (push only when requested) and note `[KB Auto-Updated: <id>]`.",
            MARKER_END,
        ]
    )


def splice_managed_block(existing_text: str, new_block: str) -> str:
    """Idempotently inserts or replaces the managed KB block in a Markdown rule file."""
    start_idx = existing_text.find(MARKER_START)
    end_idx = existing_text.find(MARKER_END)
    if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
        end_pos = end_idx + len(MARKER_END)
        return existing_text[:start_idx] + new_block + existing_text[end_pos:]

    anchor_idx = existing_text.find(SRS_END_MARKER)
    if anchor_idx != -1:
        insert_pos = anchor_idx + len(SRS_END_MARKER)
        return (
            existing_text[:insert_pos]
            + "\n\n"
            + new_block
            + existing_text[insert_pos:]
        )

    stripped = existing_text.rstrip()
    if not stripped:
        return new_block + "\n"
    return f"{stripped}\n\n---\n\n{new_block}\n"


def _copy_skill_tree(
    repo_root: pathlib.Path, dest_skill_dir: pathlib.Path, dry_run: bool
) -> None:
    src_skill_dir = repo_root / "skills" / "neuroscience-datasets"
    if not (src_skill_dir / "SKILL.md").is_file():
        raise ValueError(f"Missing source skill under {src_skill_dir}")
    if dry_run:
        logger.info("[dry-run] Would sync skill directory -> %s", dest_skill_dir)
        return
    if dest_skill_dir.exists():
        shutil.rmtree(dest_skill_dir)
    shutil.copytree(src_skill_dir, dest_skill_dir)
    query_script = dest_skill_dir / "scripts" / "query_kb.py"
    current_mode = query_script.stat().st_mode
    query_script.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    (dest_skill_dir / ".kb_root").write_text(
        f"{repo_root.resolve()}\n", encoding="utf-8"
    )


def _install_antigravity(opts: InstallOptions) -> None:
    plugin_dir = opts.home_dir / ".gemini" / "config" / "plugins" / "neuroscience-datasets"
    if opts.dry_run:
        logger.info("[dry-run] Would install Antigravity plugin -> %s", plugin_dir)
    else:
        (plugin_dir / "assets").mkdir(parents=True, exist_ok=True)
        (plugin_dir / "rules").mkdir(parents=True, exist_ok=True)
        shutil.copy2(opts.repo_root / "plugin.json", plugin_dir / "plugin.json")
        shutil.copy2(opts.repo_root / "README.md", plugin_dir / "README.md")
        shutil.copy2(
            opts.repo_root / "assets" / "logo.svg", plugin_dir / "assets" / "logo.svg"
        )
        shutil.copy2(
            opts.repo_root / "rules" / "AGENTS.md", plugin_dir / "rules" / "AGENTS.md"
        )
    _copy_skill_tree(
        opts.repo_root, plugin_dir / "skills" / "neuroscience-datasets", opts.dry_run
    )

    global_rules = opts.home_dir / ".gemini" / "config" / "rules" / "AGENTS.md"
    if global_rules.is_file():
        updated = splice_managed_block(
            global_rules.read_text(encoding="utf-8"),
            _render_antigravity_overlay_block(),
        )
        if len(updated.encode("utf-8")) <= ANTIGRAVITY_RULE_MAX_BYTES:
            if opts.dry_run:
                logger.info("[dry-run] Would update %s", global_rules)
            else:
                global_rules.write_text(updated, encoding="utf-8")
                logger.info("Updated Antigravity global rule overlay in %s", global_rules)
        else:
            logger.warning(
                "Skipped %s overlay (%d bytes > %d cap); plugin rules/AGENTS.md remains active.",
                global_rules,
                len(updated.encode("utf-8")),
                ANTIGRAVITY_RULE_MAX_BYTES,
            )
    logger.info("Synced Antigravity plugin at %s", plugin_dir)


def _install_claude(opts: InstallOptions) -> None:
    skill_dir = opts.home_dir / ".claude" / "skills" / "neuroscience-datasets"
    _copy_skill_tree(opts.repo_root, skill_dir, opts.dry_run)
    claude_md = opts.home_dir / ".claude" / "CLAUDE.md"
    existing = claude_md.read_text(encoding="utf-8") if claude_md.is_file() else ""
    updated = splice_managed_block(
        existing,
        _render_standalone_rule_block(
            "~/.claude/skills/neuroscience-datasets/SKILL.md"
        ),
    )
    if opts.dry_run:
        logger.info("[dry-run] Would update %s", claude_md)
    else:
        claude_md.parent.mkdir(parents=True, exist_ok=True)
        claude_md.write_text(updated, encoding="utf-8")
    logger.info("Synced Claude Code skill and %s", claude_md)


def _read_codex_doc_cap(codex_dir: pathlib.Path) -> int:
    cfg_toml = codex_dir / "config.toml"
    if not cfg_toml.is_file():
        return DEFAULT_CODEX_DOC_MAX_BYTES
    match = re.search(
        r"^\s*project_doc_max_bytes\s*=\s*(\d+)",
        cfg_toml.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    return int(match.group(1)) if match else DEFAULT_CODEX_DOC_MAX_BYTES


def _install_codex(opts: InstallOptions) -> None:
    codex_dir = opts.home_dir / ".codex"
    skill_dir = codex_dir / "skills" / "neuroscience-datasets"
    _copy_skill_tree(opts.repo_root, skill_dir, opts.dry_run)

    agents_md = codex_dir / "AGENTS.md"
    if not agents_md.is_file():
        return
    max_bytes = _read_codex_doc_cap(codex_dir)
    existing = agents_md.read_text(encoding="utf-8")
    updated = splice_managed_block(
        existing,
        _render_standalone_rule_block(
            "~/.codex/skills/neuroscience-datasets/SKILL.md"
        ),
    )
    if len(updated.encode("utf-8")) > max_bytes:
        logger.info(
            "Preserved %s untouched (%d bytes near %d-byte project_doc_max_bytes cap); "
            "Codex natively auto-indexes %s.",
            agents_md,
            len(existing.encode("utf-8")),
            max_bytes,
            skill_dir / "SKILL.md",
        )
        return
    if opts.dry_run:
        logger.info("[dry-run] Would update %s", agents_md)
    else:
        agents_md.write_text(updated, encoding="utf-8")
        logger.info("Updated Codex global rules in %s", agents_md)


def run_install(opts: InstallOptions) -> None:
    """Executes plugin/skill synchronization for all requested agent targets."""
    if not (opts.repo_root / "catalog" / "datasets.json").is_file():
        raise ValueError(
            f"Missing compiled catalog in {opts.repo_root}; run build_catalog.py first."
        )
    for target in opts.targets:
        if target not in ALLOWED_TARGETS:
            raise ValueError(
                f"Unknown target {target!r}; allowed={sorted(ALLOWED_TARGETS)}"
            )
    if "antigravity" in opts.targets:
        _install_antigravity(opts)
    if "claude" in opts.targets:
        _install_claude(opts)
    if "codex" in opts.targets:
        _install_codex(opts)


def _parse_args(argv: Sequence[str] | None = None) -> InstallOptions:
    parser = argparse.ArgumentParser(
        description="Install/sync neuroscience-datasets skill across Antigravity, Claude Code, and Codex CLI."
    )
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--home-dir", type=pathlib.Path, default=pathlib.Path.home())
    parser.add_argument(
        "--targets",
        type=str,
        default="all",
        help="Comma-separated list of targets (`all` or subset of `antigravity,claude,codex`).",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    raw_targets = [t.strip().lower() for t in args.targets.split(",") if t.strip()]
    targets = (
        ("antigravity", "claude", "codex")
        if raw_targets == ["all"]
        else tuple(raw_targets)
    )
    return InstallOptions(
        repo_root=args.repo_root.resolve(),
        home_dir=args.home_dir.expanduser().resolve(),
        targets=targets,
        dry_run=bool(args.dry_run),
    )


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entrypoint for multi-agent skill/plugin installation."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    opts = _parse_args(argv)
    run_install(opts)


if __name__ == "__main__":
    main()
