"""Repo-root CLI entrypoint delegating to `skills/neuroscience-datasets/scripts/query_kb.py`."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> None:
    """Loads and executes the portable skill query CLI against this repository."""
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    skill_script = (
        repo_root / "skills" / "neuroscience-datasets" / "scripts" / "query_kb.py"
    )
    spec = importlib.util.spec_from_file_location("skill_query_kb", skill_script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {skill_script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["skill_query_kb"] = module
    spec.loader.exec_module(module)
    module.main(argv)


if __name__ == "__main__":
    main()
