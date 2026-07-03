# TailorMind CRM Operator Skill

Operate the **TailorMind CRM** end-to-end through its MCP tools — the whole
lifecycle, not a single call: onboard/sync a Zoho connection, create/stage/advance
Deals and other entities through a pipeline, search + run intelligence jobs, and
manage contacts and organizations.

It teaches the **procedure and guardrails** — which tools to chain, in what order,
with what judgment — including the **"agents propose, humans commit"** trust
boundary, the multi-tenant scope contract, and the prompt-injection posture. It
ships **no credentials**; the agent brings its own instance API key.

## Install

```
npx skills add Tailor-Mind/crm-operator-skill --skill operating-crm
```

## Prerequisites

- Access to a TailorMind CRM MCP endpoint + an **instance API key** (the key binds
  the tenant; tenancy is server-derived). Configure them out-of-band — the Skill
  ships zero secrets.

## Trust boundary (why this is safe)

- **Agents propose, humans commit.** Zoho promotions go through `propose_promote_*`
  which only stage a `promote_proposals` row; a human approves in the admin UI.
  There is **no** agent-callable execute/approve/disconnect/erase tool.
- **Tenant isolation is server-enforced** from the API key.

See `skills/operating-crm/SKILL.md` + `references/` for the full procedures.
