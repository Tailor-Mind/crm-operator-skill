#!/usr/bin/env python3
"""Generate skills/operating-crm/references/tool-index.md from the contracts.

This is one of the TWO build scripts that ship with the `operating-crm` Skill
(E077 / addendum C2 — instructions-first; no operator-facing helpers in v1).

WHAT IT DOES
    Reads the canonical MCP tool registry (`contracts/mcp/tools.yaml`, the
    97-tool source of truth) and the skill manifest
    (`contracts/skill/skill.yaml`, whose `referenced_tools` list is the curated
    subset the Skill relies on). It filters the canonical tools down to the
    referenced set and emits `references/tool-index.md` — a THIN
    `name -> one-line purpose` map (plus `domain` / `api_endpoint` columns).

THE THIN-CATALOG GUARD
    `tool-index.md` is GENERATED, never hand-authored, and is the ONLY tool
    enumeration in the Skill. Recipes reference tools BY NAME only and never
    inline schemas. This script copies NO parameter schemas into the index — it
    harvests only the tool's name, domain, api_endpoint, and the first sentence
    of its canonical description (the one-line purpose).

DETERMINISM
    Output is byte-identical for unchanged inputs:
      * tools are sorted by (domain, name) — documented stable order;
      * the one-line purpose is the first sentence of the canonical
        `description`, with all interior whitespace collapsed (the YAML
        descriptions are frequently multi-line block scalars);
      * a trailing newline terminates the file.
    Re-running on unchanged contracts produces no diff (the publish drift-gate
    in T012 relies on this).

PURENESS
    stdlib + `yaml` only. ZERO MCP / FastAPI imports, no DB / network / app —
    runs in the slim `api/` venv, a bare contributor box, and CI alike.

USAGE
    python3 skills/operating-crm/scripts/generate_tool_index.py        # write
    python3 skills/operating-crm/scripts/generate_tool_index.py --stdout  # print
    python3 skills/operating-crm/scripts/generate_tool_index.py --check   # exit
                                                                          # non-zero
                                                                          # if the
                                                                          # committed
                                                                          # index is
                                                                          # stale
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.stderr.write(
        "FATAL: PyYAML is required (it is a repo dependency). Install it with "
        "`pip install pyyaml` or run this script with the api/ venv python.\n"
    )
    raise SystemExit(2)

# ---------------------------------------------------------------------------
# Path resolution — robust to cwd.
#
# This file lives at <repo>/skills/operating-crm/scripts/generate_tool_index.py,
# so the repo root is three parents up. We resolve everything relative to the
# script location, NOT the process cwd, so the script behaves identically when
# invoked from the repo root, from its own directory, or from CI.
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent  # skills/operating-crm
REPO_ROOT = SKILL_DIR.parents[1]  # <repo>

TOOLS_YAML = REPO_ROOT / "contracts" / "mcp" / "tools.yaml"
SKILL_YAML = REPO_ROOT / "contracts" / "skill" / "skill.yaml"
INDEX_MD = SKILL_DIR / "references" / "tool-index.md"

# Forward-slash, repo-relative paths used in the generated header (no absolute
# paths, no time-sensitive content — so the output is reproducible anywhere).
TOOLS_YAML_REL = "contracts/mcp/tools.yaml"
SKILL_YAML_REL = "contracts/skill/skill.yaml"
SCRIPT_REL = "skills/operating-crm/scripts/generate_tool_index.py"

_SENTENCE_END = re.compile(r"(.+?[.!?])(?:\s|$)", re.DOTALL)


def _load_yaml(path: Path) -> dict:
    """Load a YAML file, failing closed with a clear message if it is missing."""
    if not path.exists():
        raise SystemExit(f"FATAL: required contract not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise SystemExit(f"FATAL: {path} did not parse to a mapping.")
    return data


def one_line_purpose(description: str) -> str:
    """Collapse a (possibly multi-line) description to a single-sentence purpose.

    The canonical descriptions in tools.yaml are often multi-line block scalars.
    We collapse interior whitespace to single spaces and return the first
    sentence (up to and including the first . ! or ?). If no sentence terminator
    is present, the whole collapsed string is returned. NO schemas are ever
    pulled in — only this prose purpose.
    """
    collapsed = " ".join((description or "").split())
    if not collapsed:
        return ""
    match = _SENTENCE_END.match(collapsed)
    return (match.group(1) if match else collapsed).strip()


def _escape_cell(value: str) -> str:
    """Escape a value for safe inclusion in a Markdown table cell."""
    return value.replace("|", "\\|")


def build_index() -> str:
    """Read the contracts and render the deterministic tool-index markdown."""
    tools_doc = _load_yaml(TOOLS_YAML)
    skill_doc = _load_yaml(SKILL_YAML)

    tools = tools_doc.get("tools") or []
    by_name = {t["name"]: t for t in tools if isinstance(t, dict) and t.get("name")}
    canonical_count = len(by_name)

    referenced = skill_doc.get("referenced_tools") or []
    target_version = skill_doc.get("target_contract_version", "")

    # Fail closed if the manifest names a tool that is not in the canonical set.
    # (check_tool_contract.py is the dedicated drift-checker, but the generator
    # must not silently emit a half-resolved index either.)
    offenders = [name for name in referenced if name not in by_name]
    if offenders:
        raise SystemExit(
            "FATAL: skill.yaml references tools absent from "
            f"{TOOLS_YAML_REL}: {', '.join(sorted(offenders))}. "
            "Run skills/operating-crm/scripts/check_tool_contract.py for detail."
        )

    rows = [by_name[name] for name in referenced]
    # Documented stable order: sort by (domain, name). Deterministic regardless
    # of the manifest's authoring order, so byte-identical output is guaranteed.
    rows.sort(key=lambda t: (t.get("domain", ""), t["name"]))

    lines: list[str] = []
    lines.append("# Tool Index — operating-crm Skill")
    lines.append("")
    lines.append(
        "> **GENERATED FILE — DO NOT EDIT BY HAND.** Produced by "
        f"`{SCRIPT_REL}` from"
    )
    lines.append(
        f"> `{TOOLS_YAML_REL}` (the 97-tool canonical registry) filtered to "
        f"`{SKILL_YAML_REL}`'s"
    )
    lines.append(
        "> `referenced_tools`. This is the **only** tool enumeration in the "
        "Skill; recipes"
    )
    lines.append(
        "> reference tools **by name only** and never inline schemas. To change "
        "it, edit the"
    )
    lines.append(
        "> manifest and re-run the generator (or "
        "`check_tool_contract.py --regenerate`)."
    )
    lines.append(">")
    lines.append(
        f"> Tools: **{len(rows)}** referenced of **{canonical_count}** canonical."
        f" Pinned to `{TOOLS_YAML_REL}` "
        f"`target_contract_version: {target_version}`."
    )
    lines.append(">")
    lines.append("> Ordering: stable sort by `(domain, name)`.")
    lines.append("")
    lines.append("| Tool | Domain | Purpose | API endpoint |")
    lines.append("| --- | --- | --- | --- |")
    for tool in rows:
        name = _escape_cell(tool["name"])
        domain = _escape_cell(str(tool.get("domain", "")))
        purpose = _escape_cell(one_line_purpose(tool.get("description", "")))
        endpoint = _escape_cell(str(tool.get("api_endpoint", "")))
        lines.append(f"| `{name}` | {domain} | {purpose} | `{endpoint}` |")

    # Exactly one trailing newline (join + final newline) for a clean, stable
    # POSIX text file.
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the operating-crm Skill tool-index.md from the "
        "MCP + skill contracts (thin name -> purpose map; no schemas).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--stdout",
        action="store_true",
        help="print the generated index to stdout instead of writing the file.",
    )
    group.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero (without writing) if the committed tool-index.md "
        "differs from freshly generated output.",
    )
    args = parser.parse_args(argv)

    content = build_index()

    if args.stdout:
        sys.stdout.write(content)
        return 0

    if args.check:
        if not INDEX_MD.exists():
            sys.stderr.write(
                f"STALE: {INDEX_MD} does not exist; run the generator.\n"
            )
            return 1
        current = INDEX_MD.read_text(encoding="utf-8")
        if current != content:
            sys.stderr.write(
                f"STALE: {INDEX_MD.relative_to(REPO_ROOT)} is out of date. "
                "Re-run the generator (or check_tool_contract.py --regenerate).\n"
            )
            return 1
        sys.stdout.write("OK: tool-index.md is up to date.\n")
        return 0

    INDEX_MD.parent.mkdir(parents=True, exist_ok=True)
    INDEX_MD.write_text(content, encoding="utf-8")
    sys.stdout.write(
        f"Wrote {INDEX_MD.relative_to(REPO_ROOT)} "
        f"({content.count(chr(10))} lines).\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
