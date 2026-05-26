#!/usr/bin/env python3
"""
validate.py — persona-atoms catalog validator.

Checks:
  1. Each required schema file exists and is valid JSON with the expected meta-fields.
  2. Each persona composition file exists, is valid JSON, and satisfies
     the composition-v1 structural requirements.
  3. Every persona declares at least one knowledge_boundaries entry.
  4. Required design-doc files exist and exceed the minimum word count.

Exit 0 on success; non-zero on any failure.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent

REQUIRED_SCHEMAS = [
    "voice-profile-v1.json",
    "role-definition-v1.json",
    "behavioural-constraint-v1.json",
    "knowledge-boundary-v1.json",
    "tone-parameter-v1.json",
    "composition-v1.json",
    "rule-v1.json",
]

# Persona slugs that must exist under personas/
REQUIRED_PERSONAS = [
    "coding-assistant-strict",
    "research-analyst",
    "customer-support-warm",
    "devils-advocate",
    "refactor-scout",
]

# Required top-level fields in every persona composition atom.json
COMPOSITION_REQUIRED_FIELDS = [
    "schema",
    "type",
    "id",
    "version",
    "name",
    "role_definition",
    "voice_profile",
    "knowledge_boundaries",
    "tone_parameters",
]

REQUIRED_DOCS = [
    ("docs/xaip-persona-composition.md", 200),
    ("docs/distinction-from-prompt-atoms.md", 200),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ERRORS: List[str] = []
PASSES: List[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)
    print(f"  FAIL  {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    PASSES.append(msg)
    print(f"  OK    {msg}")


def load_json(path: Path) -> Tuple[Optional[Dict], Optional[str]]:
    """Return (parsed_dict, None) on success or (None, error_message) on failure."""
    try:
        with path.open() as f:
            return json.load(f), None
    except json.JSONDecodeError as exc:
        return None, f"JSON parse error: {exc}"
    except OSError as exc:
        return None, f"Cannot read file: {exc}"


# ---------------------------------------------------------------------------
# Check 1 — Schema files
# ---------------------------------------------------------------------------

def check_schemas() -> None:
    print("\n=== Schema files ===")
    schemas_dir = REPO_ROOT / "schemas"
    for name in REQUIRED_SCHEMAS:
        path = schemas_dir / name
        if not path.exists():
            fail(f"schemas/{name} — file missing")
            continue

        data, err = load_json(path)
        if err:
            fail(f"schemas/{name} — {err}")
            continue

        for meta_field in ("$schema", "$id", "title"):
            if meta_field not in data:
                fail(f"schemas/{name} — missing required meta-field '{meta_field}'")
                break
        else:
            ok(f"schemas/{name}")


# ---------------------------------------------------------------------------
# Check 2 — Persona composition files
# ---------------------------------------------------------------------------

def check_personas() -> None:
    print("\n=== Persona compositions ===")
    personas_dir = REPO_ROOT / "personas"
    for slug in REQUIRED_PERSONAS:
        atom_path = personas_dir / slug / "atom.json"
        if not atom_path.exists():
            fail(f"personas/{slug}/atom.json — file missing")
            continue

        data, err = load_json(atom_path)
        if err:
            fail(f"personas/{slug}/atom.json — {err}")
            continue

        missing = [f for f in COMPOSITION_REQUIRED_FIELDS if f not in data]
        if missing:
            fail(
                f"personas/{slug}/atom.json — missing required fields: "
                + ", ".join(missing)
            )
            continue

        # Check type is "persona"
        if data.get("type") != "persona":
            fail(
                f"personas/{slug}/atom.json — 'type' must be 'persona', "
                f"got '{data.get('type')}'"
            )
            continue

        ok(f"personas/{slug}/atom.json")


# ---------------------------------------------------------------------------
# Check 3 — boundary-coverage rule
# ---------------------------------------------------------------------------

def check_boundary_coverage() -> None:
    print("\n=== Boundary coverage rule ===")
    personas_dir = REPO_ROOT / "personas"
    for slug in REQUIRED_PERSONAS:
        atom_path = personas_dir / slug / "atom.json"
        if not atom_path.exists():
            # Already reported in check_personas
            continue

        data, err = load_json(atom_path)
        if err:
            continue

        boundaries = data.get("knowledge_boundaries")
        if not isinstance(boundaries, list) or len(boundaries) == 0:
            fail(
                f"personas/{slug}/atom.json — boundary-coverage: "
                "'knowledge_boundaries' must be a non-empty list"
            )
        else:
            ok(f"personas/{slug}/atom.json — boundary-coverage ({len(boundaries)} entries)")


# ---------------------------------------------------------------------------
# Check 4 — Required documentation files
# ---------------------------------------------------------------------------

def check_docs() -> None:
    print("\n=== Documentation files ===")
    for rel_path, min_words in REQUIRED_DOCS:
        path = REPO_ROOT / rel_path
        if not path.exists():
            fail(f"{rel_path} — file missing")
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            fail(f"{rel_path} — cannot read: {exc}")
            continue

        word_count = len(text.split())
        if word_count < min_words:
            fail(
                f"{rel_path} — too short ({word_count} words; minimum {min_words})"
            )
        else:
            ok(f"{rel_path} — {word_count} words")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("persona-atoms catalog validator")
    print(f"Repo root: {REPO_ROOT}")

    check_schemas()
    check_personas()
    check_boundary_coverage()
    check_docs()

    print(f"\n{'=' * 40}")
    print(f"Results: {len(PASSES)} passed, {len(ERRORS)} failed")

    if ERRORS:
        print("\nFailed checks:")
        for err in ERRORS:
            print(f"  - {err}")
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
