# Contributing

## Commit convention

[Conventional Commits](https://www.conventionalcommits.org/). Prefixes:
`feat:`, `fix:`, `refactor:`, `perf:`, `docs:`, `test:`, `build:`, `ci:`,
`chore:`. Subject ≤ 72 chars, imperative mood, no trailing period.

One logical change per commit.

## Labels

Labels follow the [convergent-systems-co label
standard](https://github.com/convergent-systems-co/repo-standards/blob/v1/docs/label-guide.md).
Do not invent labels; PR the standard if you need a new one.

## Pull requests

Use the PR template. Tests required for new behavior; failing test first for
bug fixes.

## Code review

Reviews ground every medium-or-higher finding in a code citation. Self-review
your own diff before requesting review.

---

## Adding a new persona composition

### What a persona is in this catalog

A persona is a **composition of component atoms** — not a monolithic prompt. It
declares a role-definition (purpose), a voice-profile (surface form), a set of
behavioural-constraints (what the persona always or never does), one or more
knowledge-boundaries (what it knows and doesn't), and a tone-parameter
(affective profile). The runtime assembles these atoms into a rendered system
prompt at call time. This means atoms can be versioned, reused across personas,
and evolved independently.

### How to add a new persona

1. **Check whether the atoms you need already exist.**
   Browse `atoms/role-definition/`, `atoms/voice-profile/`,
   `atoms/tone-parameter/`, `atoms/behavioural-constraint/`, and
   `atoms/knowledge-boundary/`. If the atom you need doesn't exist, add it
   first (see "Adding new component atoms" below).

2. **Copy the template.**
   ```bash
   cp -r personas/TEMPLATE personas/<your-slug>
   ```

3. **Fill in every field in `personas/<your-slug>/atom.json`.**
   Replace all placeholder values (see "Field reference" below). The `id` field
   must match your directory slug exactly.

4. **Validate locally.**
   ```bash
   python3 scripts/validate.py
   ```
   The script checks schemas, required fields, and boundary-coverage. Fix any
   failures before opening a PR.

5. **Open a PR** against `main` using the PR template. Title follows
   Conventional Commits: `feat(personas): add <name>`.

### Field reference for `personas/<slug>/atom.json`

| Field | Required | Description |
|---|---|---|
| `schema` | yes | Must be `"https://persona-atoms.com/schemas/composition-v1.json"` exactly. |
| `type` | yes | Must be `"persona"` exactly. |
| `id` | yes | URL-safe slug matching the directory name. Pattern: `^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$`. |
| `version` | yes | SemVer string, e.g. `"1.0.0"`. Start new personas at `1.0.0`. |
| `name` | yes | Human-readable display name, 1–80 characters. |
| `description` | no | One or two sentences explaining what this persona is for (max 500 chars). |
| `role_definition` | yes | Single atom-ref to a role-definition atom (see URI format below). |
| `voice_profile` | yes | Single atom-ref to a voice-profile atom. |
| `tone_parameters` | yes | Single atom-ref to a tone-parameter atom. |
| `behavioural_constraints` | no | Array of atom-refs. Zero or more. Persona obeys all unconditionally. |
| `knowledge_boundaries` | yes | Array of atom-refs. Must have at least one entry (boundary-coverage rule). |
| `tags` | no | Array of short lowercase strings for search and filtering. |
| `vendors` | no | Array of LLM families this persona is known to work with. Allowed values: `claude`, `gpt`, `llama`, `gemini`, `mistral`, `any`. |
| `lifecycle` | no | `draft` (default), `stable`, `deprecated`, or `archived`. |
| `license` | no | SPDX identifier, default `Apache-2.0`. |
| `provenance` | no | Object with `source`, `addedBy`, `addedAt` (ISO 8601 datetime). |

### Referencing existing component atoms

All atom references use the `persona-atoms://` URI scheme:

```
persona-atoms://atoms/<type>/<slug>
```

Where `<type>` is one of: `role-definition`, `voice-profile`, `tone-parameter`,
`behavioural-constraint`, `knowledge-boundary`.

Example:

```json
{
  "ref": "persona-atoms://atoms/role-definition/software-engineer",
  "version": "1.0.0"
}
```

The `version` field must match the version declared in the atom's own JSON file.
Use `cat atoms/<type>/<slug>.json | jq .version` to check.

### Adding new component atoms

If your persona requires an atom that doesn't exist yet, add it before
creating the persona composition.

1. **Choose the right schema.** Each atom type has its own schema in `schemas/`.
   Read the schema to understand required fields:
   - `schemas/role-definition-v1.json`
   - `schemas/voice-profile-v1.json`
   - `schemas/tone-parameter-v1.json`
   - `schemas/behavioural-constraint-v1.json`
   - `schemas/knowledge-boundary-v1.json`

2. **Create the file** at `atoms/<type>/<slug>.json`. The `$schema` value must
   match the `$id` of the schema for that atom type.

3. **Validate:** `python3 scripts/validate.py`. Then reference your new atom
   from the persona composition.

4. **Commit the new atoms in a separate commit** from the persona composition,
   using the `feat(atoms):` prefix.

### Validation

```bash
python3 scripts/validate.py
```

This script checks:
- All required schema files exist and have valid JSON with meta-fields.
- Required persona compositions exist and satisfy structural requirements.
- Every persona declares at least one `knowledge_boundaries` entry.
- Required documentation files exist and meet minimum word counts.

Exit 0 means all checks passed. Non-zero means something needs fixing.
