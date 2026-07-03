# Changelog — operating-crm Skill

All notable changes to the public distribution of the **operating-crm** Skill
(`Tailor-Mind/crm-operator-skill`) are recorded here. The version channel is the
`skill-v*` git tag cut in the private source repo (`Tailor-Mind/agentic-crm`);
`npx skills` has no semver, so each entry below maps a public release tag to the
skill's own `metadata.version` in `SKILL.md`.

This file is the **seed** that the publish pipeline
(`.github/workflows/publish-skill.yml`, E077 T012) prepends a release stanza to
on every `skill-v*` export. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/).

Install:

```
npx skills add Tailor-Mind/crm-operator-skill --skill operating-crm -a claude-code
```

<!-- PUBLISH-PIPELINE-INSERT-ABOVE -->
<!--
  The export job in publish-skill.yml inserts a new release stanza directly
  BELOW this marker (newest-first), of the shape:

    ## [skill-vX.Y.Z] — YYYY-MM-DD

    - Exported from Tailor-Mind/agentic-crm @ <commit-sha>.
    - SKILL.md metadata.version: <x.y.z>.

  Do NOT hand-author release stanzas — they are machine-generated at export.
-->

## [Unreleased]

- **Dogfood-driven ref tightening (arg-shape accuracy).** The C5 3-model dogfood
  (Haiku / Sonnet / Opus) held every safety guardrail (0 unattended writes, 0
  cross-tenant, 100% propose-gate STOPs, no fabrication) but surfaced 5 recurring
  arg-shape struggles where recipe prose did not match the live MCP wire-schemas,
  forcing trial-and-error. Tightened the recipe references (prose / arg hints only
  — **no** tool additions, `referenced_tools` manifest unchanged, generated
  `tool-index.md` untouched): (1) `create_entity` is keyed by **`entity_type_id`
  (UUID)**, not the type name — resolve it via `list_entity_types` first, and
  supply the type's **required** attributes; (2) documented **`400
  ACTOR_USER_ID_REQUIRED`** — an auto-provisioned instance key (E076) with a null
  `created_by` cannot perform governed writes; STOP and report a provisioning
  precondition rather than forging `X-Actor-User-Id`; (3) `link_contact_to_
  organization` uses **`org_id`** (not `organization_id`) + `contact_id`; (4)
  `propose_promote_contact` / `propose_promote_organization` take **`fields` as a
  dict** (field name → value), not a list, with a `dry_run: true` key-only preview
  as the safe first step; (5) `summarize_contact` requires **`interaction_ids`
  (array)** + optional `length_preference`, not `contact_id` — resolve interaction
  ids first, and if the contact has none there is nothing to summarize.
- **Reliability guardrail (anti-fabrication + capabilities boundary).** Added a
  fourth load-bearing operator-contract rule — *never fabricate an outcome*: the
  agent must not report a create/update/write/stage-change as done unless a tool
  call actually returned success, and must surface tool errors verbatim. Added a
  *Capabilities and boundaries* section stating the Skill operates records +
  reads schema but **cannot author ontology/schema** (no `create_entity_type` /
  `add_entity_field` / `create_relationship_type` / `create_pipeline` /
  `add_stage`), and redirecting schema-authoring requests to the **Schema
  Copilot** (Settings → Ontology → Copilot). Instructions-only — no change to the
  `referenced_tools` manifest.
- Initial public-distribution scaffolding (E077 W4). No `skill-v*` tag has been
  cut yet: per E077 D3 the first real publish is **HELD** until the C5 dogfood
  eval (E077 T011) is green. See `.github/workflows/publish-skill.yml`.
