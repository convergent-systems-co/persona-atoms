#!/usr/bin/env python3
"""Build exports/catalog.json from validated persona compositions and rules.

Walks personas/, atoms/, rules/; validates each against its schema; assembles
a single machine-readable catalog manifest. Exits 1 on validation failure.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schemas"
ATOMS_DIR = REPO / "atoms"
COMPOSITIONS_DIR = REPO / "personas"
RULES_DIR = REPO / "rules"
EXPORT_PATH = REPO / "exports" / "catalog.json"
CATALOG_NAME = "persona-atoms"
CATALOG_VERSION = "0.1.0"


def load_validator(name: str) -> jsonschema.Draft202012Validator:
    schema = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def collect(dir_path: Path, validator, label: str) -> list[dict]:
    if not dir_path.exists():
        return []
    out: list[dict] = []
    for path in sorted(dir_path.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(data))
        if errors:
            print(f"✗ {path.relative_to(REPO)} ({label}):", file=sys.stderr)
            for err in errors:
                loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
                print(f"    {err.message} at {loc}", file=sys.stderr)
            sys.exit(1)
        out.append(data)
    return out


def main() -> int:
    # personas/ dir holds compositions validated against composition-v1.json
    compositions = collect(COMPOSITIONS_DIR, load_validator("composition-v1.json"), "composition")
    # atoms/ and rules/ are reserved; no atom-v1 schema exists yet for persona primitives
    atoms: list[dict] = []
    rules: list[dict] = []

    catalog = {
        "catalog": CATALOG_NAME,
        "version": CATALOG_VERSION,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "atoms": atoms,
        "compositions": compositions,
        "rules": rules,
    }

    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPORT_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {EXPORT_PATH.relative_to(REPO)} — {len(atoms)} atoms, {len(compositions)} compositions, {len(rules)} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
