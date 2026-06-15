# Atoms Catalog Standard (atoms-spec)

> The canonical specification every `*-Atoms` catalog in the Convergent Systems
> ecosystem MUST conform to. Versioned (`v1`, `v2`, ...).
>
> Extracted from `aish/ARCHITECTURE.md`. The spec lives here so it can evolve
> independently of any one catalog or runtime.

---


## Atoms Catalog Standard (The Atoms Spec)

This section is the canonical specification for an `*-Atoms` catalog. It is written to be executable — a maintainer or AI agent can read this section and bootstrap a conforming catalog repository without additional documentation.

### Repository Strategy: One Repo Per Catalog

**Decision: each `*-Atoms` catalog is its own repository.** Not a monorepo.

This is mandated by the architectural principle. The ecosystem is “decentralized but cataloged” — catalogs are themselves decentralized. They can be donated to foundations, transferred to new maintainers, federated with external organizations, all independently. A monorepo couples all release cycles, all contributor communities, and all governance under one roof, which contradicts the principle.

The existing Brand Atoms repository (`github.com/convergent-systems-co/branding-library`) already follows this pattern. Future catalogs follow the same model.

**Shared standards live in dedicated spec/tooling repos:**

|Repo         |Purpose                                                                                          |
|-------------|-------------------------------------------------------------------------------------------------|
|`atoms-spec` |Canonical JSON Schemas, validation rules, and conventions every `*-Atoms` catalog must conform to|
|`atoms-tools`|CLI for validation, export generation, schema migration, catalog bootstrapping                   |
|`xdao`       |Federation portal source — directory of catalogs, governance issues, cross-catalog standards     |

Each `*-Atoms` repo declares its conformance to a specific `atoms-spec` version in its manifest. The spec evolves through governance at XDAO; catalogs migrate at their own pace.

-----

### Required Repository Structure

Every `*-Atoms` catalog repository MUST conform to this structure:

```
<name>-atoms/
├── README.md                      # Thesis, structure, usage examples
├── LICENSE                        # Apache-2.0 (ecosystem default)
├── ATOMS.yml                      # Catalog manifest (see below)
├── atoms/                         # Reusable building blocks
│   ├── <atom-type-1>/
│   │   ├── <atom-1>.yml
│   │   └── <atom-2>.yml
│   └── <atom-type-2>/
│       └── ...
├── <composition-dir>/             # Higher-level artifacts
│   │                              # Named per catalog: brands/, services/,
│   │                              # prompts/, agents/, etc.
│   ├── <composition-1>/
│   │   └── definition.yml
│   └── ...
├── rules/                         # Typed constraint vocabulary
│   ├── <rule-name-1>.yml
│   └── ...
├── schemas/                       # Catalog-specific JSON Schemas
│   ├── atom.schema.json
│   ├── composition.schema.json
│   └── rule.schema.json
├── exports/                       # Machine-readable exports (CI-generated)
│   ├── catalog.json               # Full catalog export
│   ├── tokens.json                # W3C Design Tokens if applicable
│   └── manifest.json              # Lightweight discovery manifest
├── docs/                          # Human-readable documentation
│   └── ...
└── .github/
    └── workflows/
        ├── validate.yml           # Schema + reference validation on PR
        └── publish.yml            # Regenerate exports, tag releases
```

**Naming rules:**

- Repo name: `<name>-atoms` (matches domain pattern, e.g., `prompt-atoms`)
- Domain: `<name>-atoms.com` (canonical), `<name>.xdao.co` (federation redirect)
- Composition directory name: domain-appropriate plural (`brands/`, `services/`, `prompts/`, `agents/`, `policies/`, `identities/`, `frameworks/`, `workflows/`, `knowledge-bases/`, `streams/`, `conventions/`)

-----

### ATOMS.yml Manifest

The manifest is the single source of truth for catalog metadata. Required at repo root.

```yaml
# ATOMS.yml — example for prompt-atoms

name: prompt-atoms
version: 0.1.0
spec: atoms-spec/v1
domain: prompt-atoms.com
ecosystem:
  federation: xdao.co
  redirect: prompt.xdao.co

purpose: |
  Machine-readable encyclopedia of LLM prompt fragments.

atomTypes:
  - persona
  - constraint
  - format-instruction
  - tool-use-template
  - refusal-pattern
  - output-schema

compositionType: prompts
compositionDir: prompts

ruleTypes:
  - model-compatibility
  - token-length-constraint
  - format-compatibility

runtimeConsumers:
  - aish
  - olympus

license: Apache-2.0
maintainers:
  - name: Convergent Systems
    contact: maintainers@xdao.co
```

-----

### Required Atom Schema

Every atom file MUST validate against the catalog’s `atom.schema.json`, which itself MUST extend the base atom schema in `atoms-spec`.

**Base atom schema (from `atoms-spec`):**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "type", "version", "name"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$"
    },
    "type": {
      "type": "string",
      "description": "Atom type — must be one of the catalog\u2019s declared atomTypes"
    },
    "version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "name": {
      "type": "string"
    },
    "description": { "type": "string" },
    "provenance": {
      "type": "object",
      "properties": {
        "source": { "type": "string" },
        "addedBy": { "type": "string" },
        "addedAt": { "type": "string", "format": "date-time" }
      }
    },
    "license": { "type": "string" }
  }
}
```

Catalog-specific schemas extend this with their domain-specific fields. For example, `palettes` in Brand Atoms adds `swatches`; `personas` in Prompt Atoms adds `voice` and `expertise`.

-----

### Required Exports

Every catalog MUST publish machine-readable exports on every release. Exports live in `exports/` and are CI-generated, never hand-edited.

|File           |Purpose                                                               |Format           |
|---------------|----------------------------------------------------------------------|-----------------|
|`manifest.json`|Lightweight discovery — name, version, atom counts, composition counts|JSON             |
|`catalog.json` |Full catalog dump — every atom, composition, rule                     |JSON             |
|`tokens.json`  |If catalog has design-token-applicable values (colors, sizes, spacing)|W3C Design Tokens|

Exports MUST be:

- Deterministic — same source produces byte-identical exports
- Signed — release artifacts include a detached signature
- Versioned — exports include the catalog version in the filename pattern when bundled

-----

### Required CI Workflows

Two GitHub Actions workflows are mandatory. Both consume `atoms-tools` (when it exists) for validation.

**`validate.yml`** — runs on every PR:

```yaml
name: Validate Catalog
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install atoms-tools
        run: npm install -g @convergent-systems/atoms-tools
      - name: Validate schemas
        run: atoms validate schemas
      - name: Validate atoms
        run: atoms validate atoms
      - name: Validate compositions reference real atoms
        run: atoms validate compositions
      - name: Validate rules conformance
        run: atoms validate rules
      - name: Regenerate exports (dry-run)
        run: atoms export --check
```

**`publish.yml`** — runs on release tag:

```yaml
name: Publish Catalog
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate exports
        run: atoms export
      - name: Sign exports
        run: atoms sign exports/
      - name: Create release
        uses: softprops/action-gh-release@v2
        with:
          files: exports/*
      - name: Notify XDAO federation
        run: atoms notify-federation
```

-----

### Federation Registration with XDAO

Every catalog MUST register with the XDAO federation directory. Registration is a PR to `github.com/convergent-systems-co/xdao` adding an entry to `ecosystem/catalogs.yml`:

```yaml
- name: prompt-atoms
  domain: prompt-atoms.com
  repo: https://github.com/convergent-systems-co/prompt-atoms
  manifestUrl: https://prompt-atoms.com/exports/manifest.json
  status: active   # or: proposed, deprecated, archived
  maintainers:
    - convergent-systems
```

XDAO’s dashboard discovers catalogs by reading `catalogs.yml`, fetching each manifest, and showing live status across the ecosystem.

-----

### Civilization-Grade Properties — Catalog Validation

Every catalog must satisfy the civilization-grade properties. The `validate.yml` CI workflow MUST enforce all of these:

|Property        |Validation                                                                                      |
|----------------|------------------------------------------------------------------------------------------------|
|Typed           |Every atom, composition, and rule validates against a JSON Schema                               |
|Versioned       |Every atom has a semver `version` field                                                         |
|Machine-readable|`catalog.json` export is valid JSON parseable without manual intervention                       |
|Composable      |Compositions reference atoms by ID; references resolve; circular refs forbidden                 |
|Open            |LICENSE file is OSI-approved (Apache-2.0 default)                                               |
|Durable         |No external dependencies that could disappear (no external image URLs for primary content, etc.)|

A catalog that fails any of these in CI cannot merge to main.

-----

### Bootstrap Procedure (for AI agents and humans)

To create a new `*-Atoms` catalog conforming to this specification, execute the following steps. This procedure is intentionally precise so an AI agent reading the architecture document can perform it end-to-end.

**Step 1: Decide the catalog domain**

The proposed catalog must have a clear runtime consumer in the existing ecosystem. If no runtime currently consumes it, defer.

**Step 2: Reserve the name**

- Verify `<name>-atoms.com` is owned by Convergent Systems
- Create repo `github.com/convergent-systems-co/<name>-atoms`
- Reserve `<name>.xdao.co` subdomain for federation redirect

**Step 3: Bootstrap the repository structure**

Create files per the Required Repository Structure section above. Empty `atoms/`, `<composition-dir>/`, and `rules/` directories with `.gitkeep` files are acceptable for initial commit.

**Step 4: Populate ATOMS.yml**

Use the manifest schema above. Declare `atomTypes`, `compositionType`, `ruleTypes`, and `runtimeConsumers` precisely.

**Step 5: Define the schemas**

Write `schemas/atom.schema.json`, `schemas/composition.schema.json`, `schemas/rule.schema.json`. Each extends the base schemas in `atoms-spec` and adds domain-specific fields.

**Step 6: Add CI workflows**

Copy `validate.yml` and `publish.yml` from the templates above. Adjust no logic — only the validation must be domain-agnostic.

**Step 7: Add seed content**

Create at minimum 3 atoms per declared `atomType` and 1 composition. This validates the schemas are workable and provides a starting point for contributors.

**Step 8: Generate initial exports**

Run `atoms export` (or equivalent manual JSON dump). Commit `exports/manifest.json` and `exports/catalog.json` to validate the export pipeline works end-to-end.

**Step 9: Write README**

The README MUST include:

- Thesis (one paragraph — what this catalog makes civilization-grade)
- Structure overview
- How to consume (where exports live, format)
- How to contribute (PR a new atom or composition)
- Link to XDAO and other catalogs

**Step 10: Register with XDAO**

Open a PR to `github.com/convergent-systems-co/xdao` adding the catalog to `ecosystem/catalogs.yml` with `status: proposed`. Once merged, the catalog appears in the XDAO directory.

**Step 11: First release**

Tag `v0.1.0`. The `publish.yml` workflow generates signed exports, creates a GitHub release, and notifies XDAO of the active status.

The catalog is now part of the ecosystem.

---

## persona-atoms vX.X.X — Personas, Panels, and Teams

This section defines the next intended model for `persona-atoms`. It extends the
current catalog from "single persona compositions" toward a layered system of
personas, panels, pods, and teams.

### Core model

The catalog currently treats a persona as a composition of:

- `role-definition`
- `voice-profile`
- `behavioural-constraint`
- `knowledge-boundary`
- `tone-parameter`

That remains valid, but it is no longer sufficient for agentic delivery
systems. The next model distinguishes between:

| Layer | Purpose | Example |
|-------|---------|---------|
| `persona` | One agent identity | `planner-tech-lead` |
| `work_contract` | How a persona participates in work | planner contract, reviewer contract |
| `composition` | A reusable multi-persona unit | `development-pod` |
| `team` | A higher-level orchestration composition | `development-team` |

### Definitions

#### Persona

A **persona** is a single agent identity with a class, domain, voice,
boundaries, and behavioral rules.

#### Work contract

A **work contract** defines how a persona works, not who it is. It specifies:

- inputs
- goal
- allowed actions
- forbidden actions
- output artifacts
- escalation triggers
- done criteria

`role-definition` remains the identity anchor. `work_contract` is the execution
contract.

#### Composition

A **composition** is a reusable collaboration unit made of multiple personas.
Compositions may be delivery-oriented, review-oriented, or orchestration-
oriented.

Examples:

- `development-pod`
- `security-review-panel`
- `architecture-review-panel`
- `documentation-review-panel`

#### Team

A **team** is a composition that orchestrates multiple lower-level
compositions, usually with one or more coordinators and multiple pods or
panels.

### Classes

The foundational classes for `persona-atoms` vX.X.X are:

| Class | Purpose | Decision scope |
|-------|---------|----------------|
| `planner` | Plans work, decomposes scope, proposes implementation approach | planning decisions only |
| `executor` | Produces code, tests, docs, infrastructure, or artifacts | no review decisions |
| `reviewer` | Produces content-level findings and recommendations | content-level |
| `moderator` | Orchestrates a review panel and emits aggregate panel state | panel/state-level only |
| `coordinator` | Routes work across pods, panels, and teams | workflow/routing |
| `aggregator` | Brings code, docs, reports, data, and evidence together | no decisions |

### Moderator and aggregator semantics

These roles are intentionally distinct.

#### Reviewer

A reviewer makes **content-level judgments** inside its domain.

Examples:

- identifying a security flaw
- flagging a missing architectural boundary
- rejecting inadequate documentation

#### Moderator

A moderator is a **review orchestrator**. It never performs substantive review
work. It may:

- collect review outputs
- detect missing required reviews
- identify conflicts between reviewers
- emit aggregate panel state such as `approve`, `conditional`, or `block`
- route rework back to the originating composition

A moderator must not:

- originate domain findings
- override reviewer findings at the content level
- inject its own security, architecture, documentation, or testing judgment

#### Aggregator

An aggregator performs **artifact assembly** only. It brings things together
without judging them.

Examples:

- bundling code, docs, and review reports into one delivery packet
- combining evidence across panels
- assembling a release dossier or audit package

An aggregator must not emit pass/fail decisions.

### Foundation compositions

The first compositions to standardize are the ones most common to agentic
software delivery in Claude Code, Copilot, Codex, and similar runtimes.

#### Development Pod

A **Development Pod** is the smallest reusable delivery unit.

| Member persona | Class | Role in pod |
|----------------|-------|-------------|
| `planner-tech-lead` | planner | decomposes work and defines delivery path |
| `executor-coder` | executor | produces application code |
| `executor-iac-coder` | executor | produces infrastructure code when needed |
| `executor-tdd-test-writer` | executor | writes failing contract tests first |
| `reviewer-adversarial-test-writer` | reviewer | probes for gaps, gaming, and weak coverage |
| `reviewer-test-verifier` | reviewer | validates the finished implementation against the contract |

Development Pod contract:

- **entry:** issue, batch, or scoped work item
- **flow:** plan -> tests -> implementation -> adversarial review -> verification
- **exit:** implementation ready for team-level review panels

#### Development Team

A **Development Team** is the foundational team composition for delivery.

| Member composition or persona | Function |
|--------------------------------|----------|
| `coordinator-devops-engineer` | routes work, manages capacity, merges delivery flow |
| `N x development-pod` | executes implementation workstreams |
| `executor-document-writer` | updates documentation affected by changes |
| `documentation-review-panel` | validates documentation readiness |
| `security-review-panel` | validates security readiness |
| `architecture-review-panel` | validates architecture readiness |
| `aggregator-delivery-evidence` | assembles final artifacts and evidence when required |

Development Team contract:

- **entry:** prioritized work queue
- **flow:** assign work to pods, trigger required review panels, reconcile outputs
- **exit:** reviewed, documented, validated delivery ready for merge/release

### First-build inventory

The first personas and compositions to add should be:

| Name | Kind | Class | Domain |
|------|------|-------|--------|
| `planner-tech-lead` | persona | planner | engineering |
| `executor-coder` | persona | executor | engineering |
| `executor-iac-coder` | persona | executor | infrastructure |
| `executor-tdd-test-writer` | persona | executor | testing |
| `reviewer-adversarial-test-writer` | persona | reviewer | testing |
| `reviewer-test-verifier` | persona | reviewer | testing |
| `coordinator-devops-engineer` | persona | coordinator | delivery-platform |
| `executor-document-writer` | persona | executor | documentation |
| `reviewer-documentation` | persona | reviewer | documentation |
| `reviewer-security` | persona | reviewer | security |
| `reviewer-systems-architect` | persona | reviewer | architecture |
| `moderator-review-panel` | persona | moderator | review-orchestration |
| `aggregator-delivery-evidence` | persona | aggregator | delivery-evidence |
| `development-pod` | composition | n/a | delivery |
| `documentation-review-panel` | composition | n/a | documentation-review |
| `security-review-panel` | composition | n/a | security-review |
| `architecture-review-panel` | composition | n/a | architecture-review |
| `development-team` | composition | n/a | delivery-team |

### Composition contract shape

Every composition should eventually declare:

- required members
- optional members
- entry conditions
- internal workflow
- handoff rules
- moderation or decision rules
- rework routing
- output artifacts
- done criteria

### Planned schema updates

The current schema supports only persona compositions. To support the vX.X.X
model, the catalog should add the following:

#### 1. New atom type: `work-contract`

Purpose:

- define operational behavior for a persona
- separate identity from execution semantics
- allow reuse of planner, executor, reviewer, moderator, coordinator, and
  aggregator contracts

#### 2. Extend persona composition schema

Likely addition to persona composition:

- `work_contract`
- optional classification metadata such as `class` and `domain`

#### 3. New composition schema(s)

The catalog should support higher-order compositions beyond single personas:

- `panel`
- `pod`
- `team`

These compositions should be able to declare:

- member references
- workflow ordering
- trigger conditions
- required vs optional reviewers
- moderator assignment
- output contract

#### 4. Export and catalog updates

The exports should eventually distinguish between:

- atoms
- persona compositions
- higher-order compositions

This allows runtimes to discover not only individual personas, but also
reusable delivery and review topologies.

### Non-goals

This section does **not** yet define:

- final JSON Schema field names
- final file paths for panel or team definitions
- runtime-specific execution engines
- whether every domain must support every class

Those remain implementation decisions for follow-up XAIPs or ADRs.

---

## Related

- **Federation:** [xdao.co](https://xdao.co) · [github.com/convergent-systems-co/xdao](https://github.com/convergent-systems-co/xdao)
- **Tooling:** [github.com/convergent-systems-co/atoms-tools](https://github.com/convergent-systems-co/atoms-tools) — CLI for validating, exporting, bootstrapping, and resolving catalogs that conform to this spec.
- **Umbrella:** [github.com/convergent-systems-co/atoms](https://github.com/convergent-systems-co/atoms) — every conforming catalog as a git submodule.
