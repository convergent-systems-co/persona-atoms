# persona-atoms

> Persona primitives for AI agents and LLMs — voice profiles, role definitions, behavioural constraints, knowledge boundaries, tone parameters, and work contracts. Composable persona, panel, pod, and team designs that runtimes bind to agents and delivery workflows.

`persona-atoms` is a `*-Atoms` catalog in the [Convergent Systems](https://xdao.co) ecosystem. It defines what exists in its domain — typed, versioned, machine-readable, composable, and open — so runtimes (and humans) can stand on shared infrastructure instead of reinventing it.

## Structure

```
persona-atoms/
├── ATOMS.yml              # Catalog manifest
├── atoms/                 # Reusable building blocks
├── personas/              # Single-agent persona compositions
├── compositions/          # Panels, pods, and team compositions
├── rules/                 # Typed constraint vocabulary
├── schemas/               # Catalog-specific JSON Schemas
├── exports/               # CI-generated machine-readable exports
└── docs/                  # Human-readable documentation
```

### Atom types

- `voice-profile`
- `role-definition`
- `behavioural-constraint`
- `knowledge-boundary`
- `tone-parameter`
- `work-contract`

### Composition kinds

- `persona`
- `panel`
- `pod`
- `team`

### Rule types

- `prompt-conformance`
- `boundary-coverage`
- `voice-consistency`

### Runtime consumers

`aish`, `olympus`

## How to consume

Machine-readable exports are published in [`exports/`](./exports/) on every release:

- `exports/manifest.json` — lightweight discovery (name, version, counts)
- `exports/catalog.json` — full catalog dump (every atom, persona, higher-order composition, rule)

Exports are deterministic, signed, and versioned. See [`ATOMS.yml`](./ATOMS.yml) for the manifest and the conformance spec.

## How to contribute

1. Read [`ATOMS.yml`](./ATOMS.yml) to understand the catalog's atom types, compositions, and rules.
2. Add a new atom under `atoms/<type>/`, a persona under `personas/<name>/`, or a higher-order composition under `compositions/<name>/`.
3. Open a PR. CI validates the schema, references, and exports.
4. Larger structural changes go through the [XAIP process](https://github.com/convergent-systems-co/xaips).

## Distinction from prompt-atoms

`prompt-atoms` catalogs prompt **fragments** — reusable building blocks (constraints, format instructions, tool-use templates, refusal patterns). `persona-atoms` catalogs **whole operational identities and compositions** — personas that bind voice, role, behaviour, boundaries, and work contracts, plus reusable higher-order compositions such as review panels, development pods, and teams.

## Ecosystem

- **Federation:** [xdao.co](https://xdao.co) · [github.com/convergent-systems-co/xdao](https://github.com/convergent-systems-co/xdao)
- **Spec:** [github.com/convergent-systems-co/atoms-spec](https://github.com/convergent-systems-co/atoms-spec)
- **Tools:** [github.com/convergent-systems-co/atoms-tools](https://github.com/convergent-systems-co/atoms-tools)
- **Umbrella:** [github.com/convergent-systems-co/atoms](https://github.com/convergent-systems-co/atoms) — all catalogs as submodules
- **Other catalogs:** brand-atoms, service-atoms, prompt-atoms, policy-atoms, identity-atoms, compliance-atoms, workflow-atoms, agent-atoms, knowledge-atoms, event-atoms, plugin-atoms, theme-atoms

## License

Apache-2.0 — see [`LICENSE`](./LICENSE).
