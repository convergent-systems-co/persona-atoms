# persona-atoms — Goals

> Persona primitives for AI agents and LLMs — voice profiles, role definitions, behavioural constraints, knowledge boundaries, tone parameters. Composable persona designs that runtimes bind to agents, system prompts, and conversational surfaces.

*This document is **design proposal** — no ARCHITECTURE.md source; generated based on the *-Atoms catalog pattern and the conversation context that established this catalog. Sections marked **Generated** are pattern-based and are intended as a starting point for revision, not as decided plan.*

---

## What this catalog makes civilization-grade

Personas today are duplicated everywhere: a "helpful coding assistant" lives as a system-prompt blob in every agent, every chat product, every internal tooling repo. The same persona expressed across surfaces — Slack bot, IDE assistant, Discord helper, voice agent — gets re-authored per surface with subtle drift. Voice, role, behavioural rules, and knowledge boundaries fragment across system prompts, fine-tunes, eval harnesses, and runtime configs. There is no shared vocabulary for "what makes this persona, *this* persona."

By cataloging the primitives, `persona-atoms` turns this domain from opaque-and-ephemeral to typed, versioned, composable, machine-readable, and open — the civilization-grade properties the ecosystem requires.

## What it catalogs

### Atom types

- **`voice-profile`** — Sentence-level voice characteristics (formality register, hedging tolerance, sentence-length preference, lexical choices, vocabulary domain).
- **`role-definition`** — What the persona is for (coding assistant, customer-support agent, research analyst, devil's advocate). The job-to-be-done.
- **`behavioural-constraint`** — Hard rules the persona obeys (no-fabrication, refuse-medical-advice, always-cite-sources, disclose-AI-status).
- **`knowledge-boundary`** — What the persona knows and doesn't know (domain expertise, deliberately-omitted topics, cutoff-date acknowledgments).
- **`tone-parameter`** — Affective dial settings (warmth, directness, humour, formality, empathy depth).

### Compositions: `personas`

A persona composition assembles voice-profile + role-definition + behavioural-constraints + knowledge-boundaries + tone-parameters into a complete identity an agent can assume. A persona may extend a brand-atoms brand (for voice continuity) and may reference prompt-atoms fragments (for reusable constraint language).

### Rule types

- **`prompt-conformance`** — Every persona MUST render to a deterministic system-prompt string that includes the bound voice, role, constraints, boundaries, and tone parameters.
- **`boundary-coverage`** — Every persona MUST declare at least one knowledge-boundary atom; "unbounded" is not a valid persona.
- **`voice-consistency`** — Voice-profile parameters MUST NOT contradict tone-parameter settings (e.g., `formality: high` + `humour: irreverent` requires explicit override).

## Runtime consumers

- **aish** — Future — agent personas for built-in helpers (drachma advisor, refactor scout, debug navigator). Bound via `aish persona use <id>`.
- **olympus** — Future — Pantheon Module personas; each module is one or more personas with shared behavioural constraints.

## Status & priority

**Current status:** `new`

**Priority tier:** Tier 5 — New (post-ARCHITECTURE.md), runtime pull TBD

**Trigger / activation condition:** Newly acquired domain. Activates when the first runtime needs a second persona (one persona = a string; two personas = a catalog).

## Roadmap *(Generated — milestone shapes mirror the catalog-pattern; revise as actual work begins)*

### v0.1 — Bootstrap & spec acceptance

**Goal:** Schema design. Distinction from prompt-atoms clarified. 5 seed personas covering distinct role-definitions.

**Success criterion:** A runtime can `persona resolve <id>` and receive a deterministic system-prompt string with all atoms bound. Two surfaces (e.g., aish + a chat product) render the same persona identically.

**Kill criterion:** Boundary with prompt-atoms proves too thin — personas turn out to be fragment compositions with no additional semantics; archive persona-atoms and add a `composition: persona` type to prompt-atoms.

**Work:**

- [ ] XAIP: persona composition schema with prompt-conformance rules
- [ ] Define 5 atom type schemas
- [ ] Seed 5 personas (coding-assistant-strict, research-analyst, customer-support-warm, devils-advocate, refactor-scout)
- [ ] Distinction-from-prompt-atoms design doc (what lives where)
- [ ] First runtime integration (aish or olympus)

### v0.2 — Adoption & expansion

**Goal:** Voice continuity across brands. Community contribution flow. Eval harness for persona drift.

**Work:**

- [ ] Brand-bound persona variants (extends brand-atoms for voice)
- [ ] Persona-drift eval harness (does the persona stay in character across N turns?)
- [ ] Contribution template
- [ ] 20 community personas

### v1.0 — Operational

**Goal:** Write once in persona-atoms; render identically across every runtime that consumes them. Persona swap is atomic and reversible. Cross-surface persona consistency without re-authoring.

## Concrete atom example *(Generated — illustrative, not seed content)*

```yaml
personas/refactor-scout/definition.yml
---
id: refactor-scout
type: composition
version: 1.0.0
extends_brand: { ref: brand-atoms://brands/convergent-systems-co/aish }
role: { ref: atoms/role-definition/refactor-advisor }
voice: { ref: atoms/voice-profile/terse-engineer }
constraints:
  - { ref: atoms/behavioural-constraint/no-fabrication }
  - { ref: atoms/behavioural-constraint/cite-file-line }
  - { ref: atoms/behavioural-constraint/disclose-ai-status }
boundaries:
  - { ref: atoms/knowledge-boundary/own-repo-only }
  - { ref: atoms/knowledge-boundary/no-prod-credentials }
tone:
  warmth: low
  directness: high
  humour: dry
  formality: medium
```

## Adoption strategy *(Generated)*

The first runtime that needs to ship more than one persona is the anchor consumer. persona-atoms succeeds if it stays meaningfully distinct from prompt-atoms (whole composed identities vs reusable fragments) AND if cross-runtime persona portability proves real once a second consumer integrates.

## Civilization-grade property checklist

Every catalog must satisfy these before v1.0. Failing any blocks a release.

| Property | Mechanism in this catalog |
|---|---|
| Typed | JSON Schema in `schemas/` validates every atom, composition, rule |
| Versioned | Every atom has a semver `version` field; compositions reference atoms by version-pinned ID |
| Machine-readable | `exports/catalog.json` published on every release |
| Composable | Compositions reference atoms by ID; CI verifies references resolve and no circular dependencies |
| Open | Apache-2.0 licensed; LICENSE file present |
| Durable | No external dependencies for primary content (no remote image URLs, no vendor APIs in the hot path) |

## Related

- **Spec:** [atoms-spec](https://github.com/convergent-systems-co/atoms-spec) — the canonical structure every catalog conforms to
- **Tools:** [atoms-tools](https://github.com/convergent-systems-co/atoms-tools) — CLI for validate / export / bootstrap / resolve
- **Federation:** [xdao](https://github.com/convergent-systems-co/xdao) — ecosystem directory and discovery
- **Umbrella:** [atoms](https://github.com/convergent-systems-co/atoms) — every catalog as a git submodule
- **Sibling:** [prompt-atoms](https://github.com/convergent-systems-co/prompt-atoms) — reusable prompt fragments composed by personas
- **Manifest:** [`ATOMS.yml`](./ATOMS.yml) — this catalog's machine-readable manifest
- **Standard:** [`README.md`](./README.md) — catalog overview and contribution flow
