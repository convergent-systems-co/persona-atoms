# Distinction from prompt-atoms: What Lives Where

**Version:** 0.1.0
**Status:** Accepted (v0.1 Bootstrap)

---

## The one-sentence version

**persona-atoms** is about IDENTITY (who the agent IS); **prompt-atoms** is about FRAGMENTS (what the agent SAYS).

---

## Why this distinction matters

Before this catalog existed, the ecosystem had one place to put agent-related content: prompt-atoms. Everything ended up as a `persona` type atom in prompt-atoms — a blob of text that shaped the agent's behaviour. The problem is that two very different things got conflated:

1. **Role identity** — who this agent is, what it's for, what it refuses, how it speaks. Stable. Session-scoped. Singular.
2. **Prompt fragments** — reusable text chunks that get assembled into prompts. Dynamic. Turn-scoped. Composable.

Conflating them produces personas that drift (the "persona" type in prompt-atoms has no structural guarantee that it covers all five dimensions of identity), fragments that are incorrectly scoped (a "no-fabrication" rule shouldn't be re-authored every time it's needed), and runtimes that cannot portably render a persona (because the "persona" is just a blob with no typed fields).

persona-atoms solves the identity half. prompt-atoms solves the fragment half.

---

## The core semantic difference

| Dimension | persona-atoms | prompt-atoms |
|---|---|---|
| **What it represents** | A complete agent identity | A reusable text fragment |
| **Granularity** | One composition = one whole persona | One atom = one prompt chunk |
| **Session stability** | Stable for the duration of a session | Dynamic — different atoms for different turns |
| **Required fields** | role, voice, tone, boundaries (structured types) | content (string) |
| **Rendered into** | System prompt, once, at session start | Any turn: system / user / tool / assistant |
| **Versioning unit** | The whole persona versioned together | Each fragment versioned independently |
| **Primary consumer** | Agent runtime, orchestrator | Prompt assembler, composition engine |

---

## Decision criteria: does this live in persona-atoms or prompt-atoms?

Ask these questions in order:

**1. Does it define who the agent is for the duration of a session?**
- If yes → persona-atoms.
- A persona is a role that persists. A fragment is applied at a moment.

**2. Is it stable across turns?**
- If yes → persona-atoms.
- The system prompt is rendered once at session start. Turn-level instructions go into prompt-atoms.

**3. Is it a self-contained text chunk that renders directly into a prompt turn?**
- If yes → prompt-atoms.
- Fragments are the building material. Personas are what you build.

**4. Is it shared by many different agents across many different contexts?**
- If yes → probably prompt-atoms (a reusable constraint or format instruction).
- If it's specific to one identity → persona-atoms.

**5. Is it about how to communicate, or what to say?**
- How to communicate (formality, hedging, warmth, directness) → persona-atoms (voice-profile, tone-parameter).
- What to say (output schema, tool-use template, refusal pattern) → prompt-atoms.

---

## Examples and assignments

| Content | Lives in | Rationale |
|---|---|---|
| "This agent is a security-focused code reviewer" | persona-atoms (role-definition) | Defines the agent's job-to-be-done |
| "Use professional register with medium sentences" | persona-atoms (voice-profile) | Surface-form characteristic of the agent's identity |
| "Never fabricate API methods" — as an identity rule | persona-atoms (behavioural-constraint) | Definitional to this persona; always in force |
| "Never fabricate API methods" — as a reusable fragment | prompt-atoms (constraint type) | Reusable system-prompt chunk for any agent |
| "Respond in JSON with this schema: {...}" | prompt-atoms (output-schema) | A fragment injected at specific turns |
| "Use {{tool_name}} via the following pattern:" | prompt-atoms (tool-use-template) | Parameterised fragment; requires runtime input |
| "This agent has strong knowledge of software engineering" | persona-atoms (knowledge-boundary) | Identity-level scope declaration |
| "This agent's knowledge cuts off at 2025-01-01" | persona-atoms (knowledge-boundary) | Identity-level temporal scope |
| "Acknowledge the user's emotional state before addressing the task" | persona-atoms (tone-parameter / behavioural-constraint) | Identity-level empathy directive |
| "Format citations as: [Source] URL" | prompt-atoms (format-instruction) | Reusable format fragment, not identity-specific |
| "Decline requests outside software-engineering topics" | persona-atoms (knowledge-boundary / behavioural-constraint) | Identity-level scope limit |

---

## A persona USES prompt-atoms but IS NOT a fragment

A persona composition is not a prompt fragment. It is a structured object that, when rendered, produces a system prompt. That system prompt MAY incorporate text from prompt-atoms atoms — but the persona itself does not embed the fragment text. The runtime is responsible for resolving prompt-atom references and injecting them at the appropriate turn.

The relationship is:

```
[persona-atoms composition]
        ↓ renders to
[system prompt string]
        ↑ may include text derived from
[prompt-atoms atoms]
```

The runtime controls this relationship. The persona catalog defines the identity; the prompt catalog supplies the building materials; the runtime assembles the final system message.

---

## The kill criterion

The GOALS.md for persona-atoms states a kill criterion: if the boundary with prompt-atoms proves too thin — if personas turn out to be fragment compositions with no additional semantics — archive persona-atoms and add a `composition: persona` type to prompt-atoms.

This distinction document is part of the evidence that the boundary is meaningful. The five structured atom types (role-definition, voice-profile, behavioural-constraint, knowledge-boundary, tone-parameter), the prompt-conformance rule, and the boundary-coverage rule together give persona-atoms semantics that a `content: string` field in prompt-atoms cannot express. If future work erodes this distinction (e.g., all persona fields reduce to freeform text with no typed structure), revisit the kill criterion.

---

## Related

- `schemas/composition-v1.json` — the schema that enforces the structural separation
- `docs/xaip-persona-composition.md` — the XAIP that defines the interoperation protocol
- `GOALS.md` — the kill criterion and roadmap
- [prompt-atoms catalog](https://github.com/convergent-systems-co/prompt-atoms)
