# XAIP: Persona Composition Schema with Prompt-Conformance Rules

**Type:** Cross-Atoms Integration Proposal (XAIP)
**Catalog:** persona-atoms
**Version:** 0.1.0
**Status:** Accepted (v0.1 Bootstrap)
**Authors:** Convergent Systems

---

## 1. Purpose

This document defines how persona-atoms compositions assemble the five atom types into a complete agent identity, how a persona renders to a deterministic system-prompt string (the **prompt-conformance rule**), and how persona-atoms relates to the two adjacent catalogs: **prompt-atoms** and **brand-atoms**.

An XAIP is a Cross-Atoms Integration Proposal — a formal design document that governs how two or more catalogs interoperate. This XAIP is scoped to persona-atoms v0.1 and establishes the integration contracts that future XAIPs can extend.

---

## 2. The Five Atom Types and Their Roles in a Composition

A persona composition assembles exactly five atom types. Each type has a distinct semantic role:

| Atom Type | Semantic Role | Required in Composition |
|---|---|---|
| `role-definition` | The **job-to-be-done** — what the persona is *for* | Yes (exactly one) |
| `voice-profile` | **Surface-form** characteristics — how text is shaped | Yes (exactly one) |
| `behavioural-constraint` | **Hard rules** the persona always obeys | No (zero or more) |
| `knowledge-boundary` | **Scope declaration** — what the persona knows and does not | Yes (one or more) |
| `tone-parameter` | **Affective dial** settings — warmth, directness, humour | Yes (exactly one) |

The role-definition is the anchor. Voice, tone, constraints, and boundaries all qualify the role — they do not replace it. A persona with no role-definition has no coherent identity.

---

## 3. The Prompt-Conformance Rule

**Rule:** Every persona composition MUST render to a **deterministic system-prompt string** from the bound atoms alone, without runtime input.

This is the most important rule in persona-atoms. It separates a persona (a stable identity) from a prompt template (a parameterised fragment that requires inputs to complete).

### 3.1 What "deterministic" means

Given the same persona composition at the same version:
- Two different runtimes produce byte-identical system prompts (after whitespace normalisation).
- The same runtime produces the same system prompt on every call.
- No runtime input (user message, tool output, session context) changes the rendered system prompt.

### 3.2 Rendering algorithm

The default rendering algorithm assembles the system prompt in this order:

```
[1] Role header
    Derived from: role_definition.job_to_be_done

[2] Voice directive
    Derived from: voice_profile fields (formality, hedging_tolerance, sentence_length_preference)

[3] Tone directive
    Derived from: tone_parameters fields (warmth, directness, humour, empathy_depth)

[4] Behavioural constraints block
    Derived from: each behavioural_constraint.constraint_text, in reference order

[5] Knowledge boundary block
    Derived from: each knowledge_boundary.boundary_text, in reference order

[6] Brand extension note (optional)
    Derived from: extends_brand (if present)
```

A persona MAY override this algorithm by providing a `system_prompt_template` field in its `atom.json`. The template uses Mustache-style syntax (`{{role_definition.job_to_be_done}}`, `{{voice_profile.formality}}`, etc.). If a template is provided, the renderer uses it verbatim and ignores the default algorithm.

### 3.3 Example rendered output

For the `coding-assistant-strict` persona, the default algorithm produces:

```
You are a software engineer assistant. Your job is to help users write, debug, and review code with factual precision.

Voice: Use professional register. Keep sentences medium-length. Avoid hedging — make direct claims or say you don't know.

Tone: Direct and professional. Neutral warmth. No humour. Acknowledge uncertainty without dramatising it.

Constraints:
- Never fabricate APIs, function signatures, library methods, CLI flags, or configuration keys. If you cannot verify, say so.
- Cite sources for non-obvious claims. Format: "[Library Name vX.Y] link-or-path".
- Verify that every symbol you introduce exists at the version in use. When uncertain, check documentation or flag the gap.

Knowledge boundaries:
- You have strong knowledge of software engineering: algorithms, data structures, system design, common languages and frameworks.
- You do not provide medical, legal, or financial advice. Redirect those questions explicitly.
```

This output is deterministic — the same atom versions always produce this string.

---

## 4. Relationship to prompt-atoms

### The core distinction

| Dimension | persona-atoms | prompt-atoms |
|---|---|---|
| What it represents | An **identity** — who the agent *is* | A **fragment** — what the agent *says* |
| Granularity | One composition = one whole persona | One atom = one reusable prompt chunk |
| Stability | Stable across turns (persona does not change mid-session) | Dynamic — different fragments used in different turns |
| Rendering target | System prompt (once, at session start) | System prompt, user turn, tool turn, assistant turn |

### How they interoperate

A persona composition references atoms from persona-atoms only. It does not directly embed prompt-atom content. The runtime is responsible for resolving prompt-atom references and injecting them at the appropriate turn.

The interoperation pattern:

```
persona-atoms composition
  └── renders to system prompt (turn: system)
  
prompt-atoms atoms
  └── injected by runtime at appropriate turns (system / user / tool / assistant)
```

A persona MAY reference prompt-atoms atoms as recommendations via an optional `recommended_prompt_atoms` field (not required for v0.1). This signals to runtimes which prompt fragments pair well with this persona — but the persona itself does not embed the fragment text.

### What lives in persona-atoms vs. prompt-atoms

Use this decision rule:

| Question | If yes → lives in | If no → |
|---|---|---|
| Does it define *who the agent is*? | persona-atoms | Continue |
| Does it remain stable for the duration of a session? | persona-atoms | Continue |
| Is it a fragment of text rendered into a specific turn? | prompt-atoms | — |
| Is it a reusable building block shared across many contexts? | prompt-atoms | — |

**Examples:**
- "This agent is a security-focused code reviewer" → persona-atoms (role-definition)
- "Never fabricate API methods" → persona-atoms (behavioural-constraint) when it's a *persona rule*; prompt-atoms (constraint type) when it's a *reusable system-prompt chunk* for any agent
- "Respond in JSON with this schema" → prompt-atoms (output-schema)
- "This agent uses professional register" → persona-atoms (voice-profile)

Note: a behavioural-constraint in persona-atoms and a constraint-type atom in prompt-atoms are related but distinct. The persona-atoms version is *identity-level* — it is definitional for the persona. The prompt-atoms version is *fragment-level* — it is a reusable text chunk that can be composed into any prompt. A persona may reference prompt-atoms constraints by including their text in its `constraint_text`, but it does so by value, not by reference, at v0.1.

---

## 5. Relationship to brand-atoms

A persona composition MAY extend a brand-atoms brand via the `extends_brand` field. When present:

- The persona's voice-profile is interpreted *within the brand's voice guidelines*.
- The brand's typography, register, and identity norms act as an outer envelope.
- The persona's own voice-profile can be more specific than the brand but MUST NOT contradict it.

Example: a `customer-support-warm` persona that `extends_brand: brand-atoms://brands/convergent-systems-co` inherits the Convergent Systems voice guidelines. If the brand mandates professional register and the persona specifies `formality: conversational`, the brand guideline wins unless the persona explicitly annotates the override with a rationale.

This integration is optional for v0.1. No existing personas in this release use it.

---

## 6. The Voice-Consistency Rule

**Rule:** A persona's `voice_profile.formality` and `tone_parameters` MUST NOT produce contradictory signals without an explicit override annotation.

The following pairings are **always contradictory** without override:

| voice_profile.formality | tone_parameters.humour | Contradiction |
|---|---|---|
| formal | irreverent | Yes |
| formal | playful | Yes |
| informal | none | Mild (warn, not block) |

The override annotation lives in `tone_parameters.voice_consistency_override_rationale`. If this field is set, the contradiction is accepted as intentional and the validator emits a warning rather than an error.

---

## 7. The Boundary-Coverage Rule

**Rule:** Every persona MUST declare at least one `knowledge_boundaries` entry. A persona with no knowledge boundary has an undefined scope — it is not a coherent identity.

Acceptable boundary types for v0.1:
- `domain-expertise` — the persona has strong knowledge in a named domain
- `omitted-topic` — the persona declines to engage with a topic class
- `cutoff-date` — the persona's knowledge ends at a point in time
- `access-restriction` — the persona lacks access to certain systems
- `scope-limit` — the persona restricts itself to a defined operational scope

A persona may satisfy this rule with a single broad `domain-expertise` boundary, but single-topic personas (e.g., a legal research assistant) should declare both their expertise domain and the topics they omit.

---

## 8. Schema: personas/*/atom.json

The full schema is defined in `schemas/composition-v1.json`. Key fields:

```json
{
  "schema": "https://persona-atoms.com/schemas/composition-v1.json",
  "type": "persona",
  "id": "<slug>",
  "version": "<semver>",
  "name": "<human name>",
  "description": "<one-paragraph identity statement>",
  "role_definition": { "ref": "persona-atoms://atoms/role-definition/<id>", "version": "<semver>" },
  "voice_profile":   { "ref": "persona-atoms://atoms/voice-profile/<id>",   "version": "<semver>" },
  "behavioural_constraints": [
    { "ref": "persona-atoms://atoms/behavioural-constraint/<id>", "version": "<semver>" }
  ],
  "knowledge_boundaries": [
    { "ref": "persona-atoms://atoms/knowledge-boundary/<id>", "version": "<semver>" }
  ],
  "tone_parameters": { "ref": "persona-atoms://atoms/tone-parameter/<id>", "version": "<semver>" },
  "extends_brand":   { "ref": "brand-atoms://brands/<org>/<id>",            "version": "<semver>" },
  "tags": [],
  "vendors": ["any"],
  "lifecycle": "draft",
  "license": "Apache-2.0",
  "provenance": { "source": "<org>", "addedAt": "<ISO 8601>" }
}
```

All atom references use the canonical URI form `persona-atoms://atoms/<type>/<id>`. Cross-catalog references use `<catalog>-atoms://<type>/<path>`.

---

## 9. Changelog

- **0.1.0** — Initial XAIP. Covers: five-atom composition model, prompt-conformance rendering algorithm, prompt-atoms distinction, brand-atoms extension protocol, voice-consistency rule, boundary-coverage rule.
