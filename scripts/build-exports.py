#!/usr/bin/env python3
"""Build machine-readable exports and web/public mirrors for persona-atoms."""
import json
import shutil
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
PERSONAS_DIR = REPO / "personas"
GROUP_COMPOSITIONS_DIR = REPO / "compositions"
RULES_DIR = REPO / "rules"
EXPORT_PATH = REPO / "exports" / "catalog.json"
WEB_PUBLIC_DIR = REPO / "web" / "public"
WEB_EXPORT_PATH = WEB_PUBLIC_DIR / "exports" / "catalog.json"
CATALOG_NAME = "persona-atoms"
CATALOG_VERSION = "0.1.0"

ATOM_SCHEMA_BY_TYPE = {
    "voice-profile": "voice-profile-v1.json",
    "role-definition": "role-definition-v1.json",
    "behavioural-constraint": "behavioural-constraint-v1.json",
    "knowledge-boundary": "knowledge-boundary-v1.json",
    "tone-parameter": "tone-parameter-v1.json",
    "work-contract": "work-contract-v1.json",
}


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
    out.sort(key=lambda item: (item.get("type", ""), item.get("id", "")))
    return out


def collect_atoms() -> list[dict]:
    if not ATOMS_DIR.exists():
        return []

    out: list[dict] = []
    for path in sorted(ATOMS_DIR.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        atom_type = data.get("type")
        schema_name = ATOM_SCHEMA_BY_TYPE.get(atom_type)
        if not schema_name:
            print(
                f"✗ {path.relative_to(REPO)} (atom): unsupported atom type '{atom_type}'",
                file=sys.stderr,
            )
            sys.exit(1)
        validator = load_validator(schema_name)
        errors = list(validator.iter_errors(data))
        if errors:
            print(f"✗ {path.relative_to(REPO)} (atom):", file=sys.stderr)
            for err in errors:
                loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
                print(f"    {err.message} at {loc}", file=sys.stderr)
            sys.exit(1)
        out.append(data)
    out.sort(key=lambda item: (item.get("type", ""), item.get("id", "")))
    return out


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def sync_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    if src.exists():
        shutil.copytree(src, dst)
    else:
        dst.mkdir(parents=True, exist_ok=True)


def main() -> int:
    atoms = collect_atoms()
    personas = collect(PERSONAS_DIR, load_validator("composition-v1.json"), "persona")
    compositions = collect(
        GROUP_COMPOSITIONS_DIR,
        load_validator("composition-group-v1.json"),
        "composition",
    )
    rules = collect(RULES_DIR, load_validator("rule-v1.json"), "rule")

    catalog = {
        "catalog": CATALOG_NAME,
        "version": CATALOG_VERSION,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "atoms": atoms,
        "personas": personas,
        "compositions": compositions,
        "rules": rules,
    }

    write_json(EXPORT_PATH, catalog)
    write_json(WEB_EXPORT_PATH, catalog)
    sync_tree(ATOMS_DIR, WEB_PUBLIC_DIR / "atoms")
    sync_tree(PERSONAS_DIR, WEB_PUBLIC_DIR / "personas")
    sync_tree(GROUP_COMPOSITIONS_DIR, WEB_PUBLIC_DIR / "compositions")
    sync_tree(SCHEMA_DIR, WEB_PUBLIC_DIR / "schemas")
    print(
        f"wrote {EXPORT_PATH.relative_to(REPO)} and {WEB_EXPORT_PATH.relative_to(REPO)}"
        f" — {len(atoms)} atoms, {len(personas)} personas, {len(compositions)} compositions, {len(rules)} rules"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
