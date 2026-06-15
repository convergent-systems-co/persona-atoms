# Architecture

`persona-atoms` is evolving from a catalog of single-agent persona compositions
into a layered catalog of:

1. **atoms** — reusable building blocks such as role definitions, knowledge
   boundaries, behavioural constraints, tone parameters, and work contracts
2. **personas** — single-agent identities composed from those atoms
3. **compositions** — higher-order collaboration units such as panels, pods,
   and teams

## Repository layout

```
persona-atoms/
├── atoms/               reusable atom definitions
├── personas/            single-agent persona compositions
├── compositions/        panels, pods, and team compositions
├── schemas/             JSON Schemas for atoms and compositions
├── exports/             generated catalog export
├── web/                 Astro site and static public mirrors
└── scripts/             validation and export tooling
```

## Conceptual layers

| Layer | Purpose | Examples |
| --- | --- | --- |
| atoms | reusable primitives | `role-definition`, `knowledge-boundary`, `work-contract` |
| personas | one agent identity | `planner-tech-lead`, `reviewer-security` |
| compositions | reusable collaboration units | `development-pod`, `security-review-panel` |
| teams | orchestration compositions | `development-team` |

## Workflow semantics

- **reviewers** make content-level findings
- **moderators** orchestrate panels and emit aggregate panel state
- **aggregators** assemble artifacts and evidence without making decisions
- **coordinators** route work across pods, panels, and teams

## Export and website flow

`scripts/build-exports.py` validates atoms, personas, and higher-order
compositions, writes `exports/catalog.json`, and mirrors catalog JSON plus
schemas into `web/public/` so the site can serve canonical machine-readable
artifacts directly.

## Foundation compositions

The first standard compositions are:

- `development-pod`
- `documentation-review-panel`
- `security-review-panel`
- `architecture-review-panel`
- `development-team`

These define the baseline topology for agentic delivery workflows in
Copilot, Claude Code, Codex, and related runtimes.
