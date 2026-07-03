#!/usr/bin/env python3
"""Local drift-check for the operating-crm Skill's tool contract.

This is the second of the TWO build scripts that ship with the Skill (E077 /
addendum C2). It is the LOCAL-DEV mirror of the T003 CI conformance test
(`api/tests/unit/contracts/test_skill_tool_refs_in_mcp_registry.py`) — runnable
by hand at the desk so drift is caught before a push, not only in CI.

WHAT IT CHECKS (exit non-zero on ANY drift)
    1. Forward assert — REFERENCED ⊆ CANONICAL.
       REFERENCED = set(skill.yaml `referenced_tools`)
       CANONICAL  = {t.name for t in tools.yaml `tools`}
       Any referenced tool absent from the canonical registry is an OFFENDER;
       the script names each offender and points at contracts/mcp/tools.yaml.
       (This is the exact leg T003 owns in CI; the dev script shares it so the
       local check and the CI gate can never disagree.)

    2. Index staleness — the committed references/tool-index.md must byte-match
       freshly generated output. A stale index (recipe added a tool to the
       manifest but forgot to regenerate, or someone hand-edited the index)
       fails here before the T003 index-consistency assert fails in CI.

    It ALSO reports informational adds / removes between the manifest and the
    canonical set (referenced-but-fine, and the canonical tools NOT referenced)
    so a maintainer can see the shape of the relationship, not just the failures.

FIX PATH
    --regenerate rewrites references/tool-index.md in place (then re-checks).

PURENESS
    stdlib + `yaml` only, via the sibling generator. ZERO MCP / FastAPI imports,
    no DB / network. Runs in the slim api/ venv, a bare contributor box, and CI.

USAGE
    python3 skills/operating-crm/scripts/check_tool_contract.py
    python3 skills/operating-crm/scripts/check_tool_contract.py --regenerate
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Share the generator's path resolution, YAML loading, and index rendering so
# the two scripts can never drift from each other.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_tool_index as gen  # noqa: E402  (after sys.path tweak)


def _load_sets() -> tuple[list[str], set[str]]:
    """Return (referenced_list, canonical_name_set) from the two contracts."""
    tools_doc = gen._load_yaml(gen.TOOLS_YAML)
    skill_doc = gen._load_yaml(gen.SKILL_YAML)
    referenced = list(skill_doc.get("referenced_tools") or [])
    canonical = {
        t["name"]
        for t in (tools_doc.get("tools") or [])
        if isinstance(t, dict) and t.get("name")
    }
    return referenced, canonical


def check_forward_assert(referenced: list[str], canonical: set[str]) -> list[str]:
    """REFERENCED ⊆ CANONICAL. Returns the sorted offender list (empty == clean)."""
    return sorted({name for name in referenced if name not in canonical})


def check_index_stale() -> bool:
    """True if the committed tool-index.md is missing or out of date."""
    if not gen.INDEX_MD.exists():
        return True
    return gen.INDEX_MD.read_text(encoding="utf-8") != gen.build_index()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local drift-check: assert the Skill's referenced_tools are "
        "all in the MCP registry and the generated tool-index is fresh.",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="rewrite references/tool-index.md in place (the fix path), then "
        "re-run the checks.",
    )
    args = parser.parse_args(argv)

    referenced, canonical = _load_sets()

    rel_tools = gen.TOOLS_YAML_REL
    rel_skill = gen.SKILL_YAML_REL
    rel_index = gen.INDEX_MD.relative_to(gen.REPO_ROOT).as_posix()

    print(
        f"Checking {rel_skill} referenced_tools "
        f"({len(referenced)}) against {rel_tools} canonical ({len(canonical)})."
    )

    # ---- 1. Forward assert: REFERENCED ⊆ CANONICAL --------------------------
    offenders = check_forward_assert(referenced, canonical)
    if offenders:
        print("")
        print("DRIFT — referenced tools NOT in the canonical MCP registry:")
        for name in offenders:
            print(f"  - {name}   (missing from {rel_tools})")
        print("")
        print(
            f"FIX: add the tool(s) to {rel_tools}, or correct the name in "
            f"{rel_skill}'s referenced_tools."
        )
        return 1

    print(f"OK: all {len(referenced)} referenced tools are in {rel_tools}.")

    # Informational shape report (not a failure) — what the manifest covers vs
    # the rest of the canonical surface.
    not_referenced = sorted(canonical - set(referenced))
    print(
        f"INFO: {len(referenced)} of {len(canonical)} canonical tools are "
        f"referenced; {len(not_referenced)} are not (expected — v1 covers the "
        "Core-5 domains)."
    )

    # ---- 2. Index staleness -------------------------------------------------
    if args.regenerate:
        rc = gen.main([])  # writes references/tool-index.md
        if rc != 0:
            return rc

    if check_index_stale():
        print("")
        print(f"DRIFT — {rel_index} is stale (missing or out of date).")
        print(
            "FIX: re-run skills/operating-crm/scripts/generate_tool_index.py "
            "(or this script with --regenerate)."
        )
        return 1

    print(f"OK: {rel_index} is up to date.")
    print("")
    print("CLEAN: referenced ⊆ canonical AND tool-index is fresh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
