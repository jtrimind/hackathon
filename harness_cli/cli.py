#!/usr/bin/env python3
"""Small dependency-free CLI for a feature-at-a-time coding agent workflow."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from importlib import resources

ROOT = Path.cwd()
REGISTRY = ROOT / "features.json"
FEATURES_DIR = ROOT / "features"
REQUIREMENTS_DIR = ROOT / "requirements"
VALID_STATES = {"planned", "in_progress", "done"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIREMENT_ID_RE = re.compile(r"^(?:FR|NFR)-\d{3,}$")
REQUIREMENT_ID_SEARCH_RE = re.compile(r"\b(?:FR|NFR)-\d{3,}\b")


class HarnessError(Exception):
    pass


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_registry():
    data = read_json(REGISTRY)
    if not isinstance(data, dict) or not isinstance(data.get("features"), list):
        raise HarnessError("features.json must contain a features array")
    return data


def get_feature(fid, registry=None):
    registry = registry or load_registry()
    matches = [f for f in registry["features"] if f.get("id") == fid]
    if not matches:
        raise HarnessError(f"Unknown feature: {fid}")
    return matches[0]


def spec_path(feature):
    path = (ROOT / feature.get("spec", "")).resolve()
    if ROOT not in path.parents or path.suffix != ".json":
        raise HarnessError(f"Unsafe or invalid spec path for {feature.get('id')}")
    return path


def load_spec(feature):
    return read_json(spec_path(feature))


def revision(spec):
    """Hash user-approved content, excluding the approval record itself."""
    payload = {k: v for k, v in spec.items() if k != "approval"}
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_requirement_ids():
    """Return requirement IDs declared in Markdown files under requirements/."""
    ids = set()
    if not REQUIREMENTS_DIR.exists():
        return ids
    for path in REQUIREMENTS_DIR.rglob("*.md"):
        try:
            content = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            relative = path.relative_to(ROOT)
            raise HarnessError(f"Cannot read {relative}: {exc}") from exc
        ids.update(REQUIREMENT_ID_SEARCH_RE.findall(content))
    return ids


def check_requirement_links(feature, spec, known_ids):
    issues = []
    fid = feature.get("id", "<unknown>")
    refs = spec.get("requirement_ids")
    is_active = feature.get("status") in {"planned", "in_progress"}

    if refs is None:
        if is_active:
            issues.append(f"{fid}: requirement_ids must include at least one FR-NNN or NFR-NNN ID")
        return issues
    if not isinstance(refs, list):
        issues.append(f"{fid}: requirement_ids must be an array")
        return issues
    if is_active and not refs:
        issues.append(f"{fid}: requirement_ids must include at least one FR-NNN or NFR-NNN ID")

    seen = set()
    for requirement_id in refs:
        if not isinstance(requirement_id, str) or not REQUIREMENT_ID_RE.fullmatch(requirement_id):
            issues.append(f"{fid}: invalid requirement ID {requirement_id!r}; expected FR-NNN or NFR-NNN")
            continue
        if requirement_id in seen:
            issues.append(f"{fid}: duplicate requirement ID {requirement_id}")
            continue
        seen.add(requirement_id)
        if requirement_id not in known_ids:
            issues.append(f"{fid}: unknown requirement ID {requirement_id}")
    return issues


def check_spec(feature, spec, known_requirement_ids=None):
    issues = []
    if spec.get("id") != feature.get("id"):
        issues.append("spec id does not match registry")
    if not spec.get("title", "").strip():
        issues.append("title is empty")
    if not spec.get("goal", "").strip() or "TBD" in spec.get("goal", "").upper():
        issues.append("goal is empty or TBD")
    if not spec.get("in_scope") or any("TBD" in str(x).upper() for x in spec.get("in_scope", [])):
        issues.append("in_scope must contain resolved items")
    if not spec.get("acceptance_criteria") or any("TBD" in str(x).upper() for x in spec.get("acceptance_criteria", [])):
        issues.append("acceptance_criteria must contain resolved items")
    if not spec.get("verification"):
        issues.append("verification must contain at least one command")
    elif any(not str(x).strip() for x in spec["verification"]):
        issues.append("verification commands cannot be empty")
    if known_requirement_ids is None:
        known_requirement_ids = load_requirement_ids()
    issues.extend(check_requirement_links(feature, spec, known_requirement_ids))
    return issues


def validate():
    reg = load_registry()
    issues = []
    try:
        known_requirement_ids = load_requirement_ids()
    except HarnessError as exc:
        issues.append(str(exc))
        known_requirement_ids = set()
    ids = []
    positions = {f.get("id"): i for i, f in enumerate(reg["features"])}
    for i, f in enumerate(reg["features"]):
        fid = f.get("id", "")
        if not ID_RE.fullmatch(fid):
            issues.append(f"feature #{i + 1}: invalid id {fid!r}")
        if fid in ids:
            issues.append(f"duplicate feature id: {fid}")
        ids.append(fid)
        if f.get("status") not in VALID_STATES:
            issues.append(f"{fid}: invalid status")
        for dep in f.get("depends_on", []):
            if dep not in [x.get("id") for x in reg["features"]]:
                issues.append(f"{fid}: unknown dependency {dep}")
            elif positions[dep] >= i:
                issues.append(f"{fid}: prerequisite {dep} must appear earlier in features.json")
        try:
            spec = load_spec(f)
            if spec.get("id") != fid:
                issues.append(f"{fid}: spec id mismatch")
            issues.extend(check_requirement_links(f, spec, known_requirement_ids))
        except HarnessError as exc:
            issues.append(str(exc))
    # Detect cycles independently of display order.
    graph = {f.get("id"): f.get("depends_on", []) for f in reg["features"]}
    visiting, visited = set(), set()
    def visit(node):
        if node in visiting:
            issues.append(f"dependency cycle involving {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph:
                visit(dep)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
    return issues


def ensure_prerequisites(feature, registry):
    for dep_id in feature.get("depends_on", []):
        dep = get_feature(dep_id, registry)
        if dep.get("status") != "done":
            raise HarnessError(f"Prerequisite {dep_id} is {dep.get('status')}, not done")


def cmd_add(args):
    reg = load_registry()
    if not ID_RE.fullmatch(args.id):
        raise HarnessError("id must use lowercase letters, numbers, and hyphens")
    if any(f.get("id") == args.id for f in reg["features"]):
        raise HarnessError(f"Feature already exists: {args.id}")
    for dep in args.depends_on:
        get_feature(dep, reg)
    spec_rel = f"features/{args.id}.json"
    feature = {"id": args.id, "title": args.title, "depends_on": args.depends_on, "status": "planned", "spec": spec_rel}
    spec = {"id": args.id, "title": args.title, "goal": "TBD: the user-visible outcome", "in_scope": ["TBD"], "out_of_scope": [], "acceptance_criteria": ["TBD"], "verification": [], "approval": None}
    FEATURES_DIR.mkdir(exist_ok=True)
    write_json(ROOT / spec_rel, spec)
    # Insert after all dependencies while preserving a valid topological order.
    last_dep = max((next(i for i, f in enumerate(reg["features"]) if f["id"] == d) for d in args.depends_on), default=-1)
    reg["features"].insert(last_dep + 1, feature)
    write_json(REGISTRY, reg)
    print(f"Added {args.id}. Edit {spec_rel} to complete its spec.")


def cmd_status(_args):
    reg = load_registry()
    if not reg["features"]:
        print("No features yet. Discuss the MVP, then add the first feature.")
    for f in reg["features"]:
        deps = ", ".join(f.get("depends_on", [])) or "none"
        print(f"{f['id']}: {f['status']} | depends on: {deps}")


def cmd_validate(_args):
    issues = validate()
    if issues:
        print("Validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("Harness files are valid.")
    return 0


def cmd_ready(args):
    reg = load_registry()
    f = get_feature(args.id, reg)
    ensure_prerequisites(f, reg)
    if f.get("status") != "planned":
        raise HarnessError(f"Feature must be planned, currently {f.get('status')}")
    spec = load_spec(f)
    issues = check_spec(f, spec, load_requirement_ids())
    if issues:
        raise HarnessError("Spec is not ready: " + "; ".join(issues))
    print(f"{args.id} is ready for user review and approval.")


def cmd_approve(args):
    if not args.by_user:
        raise HarnessError("Approval must be explicitly confirmed by the user; pass --by-user only after they approve this exact spec.")
    reg = load_registry()
    f = get_feature(args.id, reg)
    ensure_prerequisites(f, reg)
    spec = load_spec(f)
    issues = check_spec(f, spec, load_requirement_ids())
    if issues:
        raise HarnessError("Spec is not ready: " + "; ".join(issues))
    spec["approval"] = {"by": "user", "at": datetime.now(timezone.utc).isoformat(), "revision": revision(spec)}
    write_json(spec_path(f), spec)
    print(f"Recorded user approval for {args.id} ({spec['approval']['revision'][:12]}).")


def cmd_start(args):
    reg = load_registry()
    f = get_feature(args.id, reg)
    ensure_prerequisites(f, reg)
    spec = load_spec(f)
    approval = spec.get("approval") or {}
    if approval.get("by") != "user" or approval.get("revision") != revision(spec):
        raise HarnessError("No current approval for this spec. Get explicit user approval, then run approve.")
    if f.get("status") != "planned":
        raise HarnessError(f"Feature must be planned, currently {f.get('status')}")
    f["status"] = "in_progress"
    write_json(REGISTRY, reg)
    print(f"Started {args.id}. Implement this feature only.")


def cmd_done(args):
    reg = load_registry()
    f = get_feature(args.id, reg)
    if f.get("status") != "in_progress":
        raise HarnessError(f"Feature must be in_progress, currently {f.get('status')}")
    f["status"] = "done"
    write_json(REGISTRY, reg)
    print(f"Marked {args.id} done. Report verification evidence before selecting the next feature.")


def cmd_init(_args):
    """Create a blank project scaffold without overwriting existing files."""
    try:
        template_root = resources.files("harness_cli").joinpath("templates")
    except (ModuleNotFoundError, TypeError) as exc:
        raise HarnessError("Scaffold templates are unavailable; install the packaged harness command") from exc

    def iter_files(folder, prefix=Path()):
        for item in folder.iterdir():
            relative = prefix / item.name
            if item.is_dir():
                yield from iter_files(item, relative)
            elif item.is_file():
                yield item, relative

    created, preserved = [], []
    for source, relative in iter_files(template_root):
        destination = ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_text(encoding="utf-8")
        if relative.as_posix() == "AGENTS.md":
            marker_start = "<!-- hackathon-harness:start -->"
            marker_end = "<!-- hackathon-harness:end -->"
            block = content.strip()
            if destination.exists():
                if not destination.is_file():
                    preserved.append(relative.as_posix() + " (not a regular file)")
                    continue
                existing = destination.read_text(encoding="utf-8")
                if marker_start in existing and marker_end in existing:
                    start = existing.index(marker_start)
                    end = existing.index(marker_end, start) + len(marker_end)
                    updated = existing[:start].rstrip() + "\n\n" + block + existing[end:]
                    if updated != existing:
                        destination.write_text(updated.rstrip() + "\n", encoding="utf-8")
                    preserved.append(relative.as_posix())
                elif marker_start in existing or marker_end in existing:
                    preserved.append(relative.as_posix() + " (incomplete harness markers; manual merge needed)")
                else:
                    destination.write_text(existing.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
                    created.append(relative.as_posix() + " (appended harness instructions)")
            else:
                destination.write_text(block + "\n", encoding="utf-8")
                created.append(relative.as_posix())
            continue
        if destination.exists():
            preserved.append(relative.as_posix())
            continue
        destination.write_text(content, encoding="utf-8")
        created.append(relative.as_posix())

    print(f"Initialized harness in {ROOT}")
    if created:
        print("Created:")
        for path in created:
            print(f"- {path}")
    if preserved:
        print("Preserved existing files (review if they should be integrated):")
        for path in preserved:
            print(f"- {path}")
    print("Next: review requirements/ and MVP.md, then run `harness validate`.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("status"); p.set_defaults(func=cmd_status)
    p = sub.add_parser("validate"); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("add"); p.add_argument("id"); p.add_argument("--title", required=True); p.add_argument("--depends-on", default="", help="comma-separated prerequisite IDs"); p.set_defaults(func=cmd_add)
    p = sub.add_parser("ready"); p.add_argument("id"); p.set_defaults(func=cmd_ready)
    p = sub.add_parser("approve"); p.add_argument("id"); p.add_argument("--by-user", action="store_true"); p.set_defaults(func=cmd_approve)
    p = sub.add_parser("start"); p.add_argument("id"); p.set_defaults(func=cmd_start)
    p = sub.add_parser("done"); p.add_argument("id"); p.set_defaults(func=cmd_done)
    p = sub.add_parser("init", help="initialize the harness in the current directory"); p.set_defaults(func=cmd_init)
    args = parser.parse_args()
    if hasattr(args, "depends_on"):
        args.depends_on = [x.strip() for x in args.depends_on.split(",") if x.strip()]
    try:
        result = args.func(args)
        return result if isinstance(result, int) else 0
    except HarnessError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
