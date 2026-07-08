# Tool Index — operating-crm Skill

> **GENERATED FILE — DO NOT EDIT BY HAND.** Produced by `skills/operating-crm/scripts/generate_tool_index.py` from
> `contracts/mcp/tools.yaml` (the 97-tool canonical registry) filtered to `contracts/skill/skill.yaml`'s
> `referenced_tools`. This is the **only** tool enumeration in the Skill; recipes
> reference tools **by name only** and never inline schemas. To change it, edit the
> manifest and re-run the generator (or `check_tool_contract.py --regenerate`).
>
> Tools: **37** referenced of **97** canonical. Pinned to `contracts/mcp/tools.yaml` `target_contract_version: 1.0.0`.
>
> Ordering: stable sort by `(domain, name)`.

| Tool | Domain | Purpose | API endpoint |
| --- | --- | --- | --- |
| `create_action_item` | action_items | Create a new ActionItem entity attached to a subject entity (Contact / Organization / Pilot / etc.) via the ``action_item_for_<subject_entity_type>`` relationship type. | `POST /api/v1/action-items` |
| `list_channels` | channels | List configured communication channels for the instance. | `GET /api/v1/config/channels` |
| `create_contact` | contacts | Create a new contact in the CRM | `POST /api/v1/contacts` |
| `get_contact` | contacts | Fetch a contact by ID with full profile data | `GET /api/v1/contacts/{contact_id}` |
| `list_contacts` | contacts | List contacts with optional search and filters | `GET /api/v1/contacts` |
| `create_entity` | entity | Create a new entity row of any registered type. | `POST /api/v1/entities` |
| `get_entity` | entity | Retrieve a single entity by ID. | `GET /api/v1/entities/{entity_id}` |
| `get_entity_schema` | entity | Get the full schema for a single entity type by UUID. | `GET /api/v1/config/entity-types` |
| `list_entities` | entity | List entities with filtering, pagination, and search. | `GET /api/v1/entities` |
| `list_entity_types` | entity | List entity types registered for the instance. | `GET /api/v1/config/entity-types` |
| `patch_entity` | entity | Partial update of entity properties (PATCH semantics). | `PATCH /api/v1/entities/{entity_id}` |
| `get_zoho_connection_status` | integrations | Read the current Zoho sync health snapshot for this instance. | `GET /api/v1/integrations/zoho/health` |
| `list_zoho_field_mappings` | integrations | List the customer-configured Zoho field mappings for a module (E047). | `GET /api/v1/integrations/zoho/field-mappings` |
| `list_zoho_fields` | integrations | List the Zoho fields available for a module with writability metadata (E047). | `GET /api/v1/integrations/zoho/zoho-fields` |
| `propose_promote_contact` | integrations | Propose a contact promotion for human approval (E048 T008). | `POST /api/v1/integrations/zoho/promote-proposals` |
| `propose_promote_organization` | integrations | Propose an organization (Account) promotion for human approval (E048 T008). | `POST /api/v1/integrations/zoho/promote-proposals` |
| `trigger_zoho_sync` | integrations | Force an out-of-band Zoho sync poll cycle for one or more modules (E048 T007). | `POST /api/v1/integrations/zoho/sync/retry` |
| `create_interaction` | interactions | Log a new interaction (call, note, meeting, message, or task) | `POST /api/v1/interactions` |
| `get_interaction` | interactions | Fetch a single interaction with details and participants | `GET /api/v1/interactions/{interaction_id}` |
| `list_interactions` | interactions | List interactions with optional filters | `GET /api/v1/interactions` |
| `propose_alias` | ontology | Register an ontology type alias routing a variant name to a canonical type (audit-only direct create, no approve step). | `POST /api/v1/ontology/aliases` |
| `propose_merge_types` | ontology | Propose merging one ontology type into another for HUMAN approval; returns the persisted proposal id + a PII-safe KEY-ONLY dry-run diff (summary counts, no record data). | `POST /api/v1/ontology/merge-proposals` |
| `create_organization` | organizations | Create a local-only organization. | `POST /api/v1/organizations` |
| `get_organization` | organizations | Fetch an organization by ID with full profile | `GET /api/v1/organizations/{org_id}` |
| `link_contact_to_organization` | organizations | Link a contact to an organization via the WORKS_AT junction with full-shape attributes (role / department / is_primary / is_current / started_at / ended_at). | `POST /api/v1/organizations/{org_id}/contacts` |
| `list_organizations` | organizations | List organizations with optional search | `GET /api/v1/organizations` |
| `unlink_contact_from_organization` | organizations | Unlink a contact from an organization (soft-transition). | `DELETE /api/v1/organizations/{org_id}/contacts/{contact_id}` |
| `advance_entity_stage` | pipeline | Advance a polymorphic entity to a new stage within the same pipeline. | `POST /api/v1/pipelines/{pipeline_id}/entities/{entity_id}/advance` |
| `assign_entity_to_stage` | pipeline | Assign a polymorphic entity (Contact / Pilot / Invoice / any registered type) to a pipeline stage. | `POST /api/v1/pipelines/{pipeline_id}/entities/{entity_id}/assign` |
| `get_pipeline` | pipeline | Get a single pipeline with its ordered stage list. | `GET /api/v1/config/pipelines/{pipeline_id}` |
| `list_pipelines` | pipeline | List pipelines (with their stages) configured for the instance. | `GET /api/v1/config/pipelines` |
| `get_key_metrics` | reports | CRM health metrics (contact counts, activity, pipeline, freshness) | `GET /api/v1/metrics` |
| `list_followups` | reports | Pending follow-up interactions with due dates | `GET /api/v1/interactions/followups` |
| `full_text_search` | search | Search across contacts, organizations, and interactions using full-text matching | `POST /api/v1/search` |
| `semantic_search` | search | Find conceptually similar content using AI embeddings | `POST /api/v1/search/semantic` |
| `summarize_contact` | search | Generate an AI summary from a contact's interaction history | `POST /api/v1/ai/summarize` |
| `summarize_conversation` | search | Generate an AI summary of a conversation thread | `POST /api/v1/ai/summarize` |
