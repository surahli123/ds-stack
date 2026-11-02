#!/usr/bin/env python3
"""Audit a work project for what ds-stack needs, list the gaps, and write questions for the metric owners.

    python3 tools/audit.py [--overlay DIR] [--project DIR] [--db FILE] [--out ds-ready] [--json report.json]

It reads, and never writes, the overlay ($DS_OVERLAY_DIR): metrics.json, tables.json, runner.json,
reviewers.json and denylist.txt. It reads the project folder (default: the current one): its AGENTS.md, and the
query logs and readouts of past analyses under it, to see which tables and metrics the work actually uses. With
--db it also checks that each metric's source table and columns exist (SQLite reference; a warehouse port
replaces table_columns()).

Each gap is "blocking" (ds-mode can't be trusted on this project until it is fixed) or "recommended". For each
metric owner it writes ds-ready/questions-<owner>.md: what to confirm or supply, metric by metric and table by
table. Metric definitions are a person's to write: the audit asks, it never drafts one.

Exit code: 0 no blocking gap, 1 at least one, 3 usage error.
"""

import argparse
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))

METRIC_REQUIRED = ("numerator", "denominator", "filters", "grain", "source", "owner")
METRIC_RECOMMENDED = ("verified", "pitfalls", "aliases")
UNAVAILABLE_REQUIRED = ("note", "owner")
TABLE_FIELDS = ("grain", "keys", "complete_when", "owner", "pitfalls")
SQL_TABLE = re.compile(r"\b(?:from|join)\s+([A-Za-z_][\w.]*)", re.I)
METRIC_LINE = re.compile(r"^\s*[-*]?\s*(?:metric|指标)\s*[:：]\s*(.+)$", re.I | re.M)
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "ds-ready", "ds-interrogate"}
MAX_FILES = 5000


def gap(severity, area, message, owner=None, question=None):
    return {"severity": severity, "area": area, "message": message, "owner": owner, "question": question}


def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# --- the overlay ---------------------------------------------------------------------------------------------

def audit_overlay(overlay):
    gaps, metrics, tables = [], {}, {}
    if not overlay:
        return [gap("blocking", "overlay", "DS_OVERLAY_DIR isn't set: ds-mode has no team definitions and labels every "
                                           "metric [guess]")], metrics, tables
    if not os.path.isdir(overlay):
        return [gap("blocking", "overlay", f"the overlay folder {overlay} doesn't exist")], metrics, tables
    path = os.path.join(overlay, "metrics.json")
    if not os.path.exists(path):
        gaps.append(gap("blocking", "metrics", "metrics.json is missing: the agent will invent metric definitions"))
    else:
        try:
            metrics = load_json(path)
        except ValueError as err:
            return gaps + [gap("blocking", "metrics", f"metrics.json isn't valid JSON: {err}")], {}, tables
        if not isinstance(metrics, dict) or not metrics:
            gaps.append(gap("blocking", "metrics", "metrics.json defines no metric"))
            metrics = {}
        for key, entry in metrics.items():
            gaps += audit_metric(key, entry)
    tables_path = os.path.join(overlay, "tables.json")
    if os.path.exists(tables_path):
        try:
            tables = load_json(tables_path)
        except ValueError as err:
            gaps.append(gap("blocking", "tables", f"tables.json isn't valid JSON: {err}"))
    for name, severity, why in (("runner.json", "recommended", "the query runner uses its defaults"),
                                ("reviewers.json", "recommended", "ds-interrogate uses Codex and Claude Code by default; "
                                                                  "list the CLIs approved for company data"),
                                ("denylist.txt", "recommended", "the commit hooks block every commit until it exists")):
        if not os.path.exists(os.path.join(overlay, name)):
            gaps.append(gap(severity, "overlay", f"{name} is missing: {why}"))
    denylist = os.path.join(overlay, "denylist.txt")
    if os.path.exists(denylist) and not [l for l in open(denylist, encoding="utf-8") if l.strip() and not l.startswith("#")]:
        gaps.append(gap("recommended", "overlay", "denylist.txt lists no term: add codenames and internal table names"))
    return gaps, metrics, tables


def audit_metric(key, entry):
    if not isinstance(entry, dict):
        return [gap("blocking", "metrics", f"{key}: the entry isn't an object")]
    owner = entry.get("owner")
    if entry.get("available") is False:
        missing = [f for f in UNAVAILABLE_REQUIRED if not entry.get(f)]
        return [gap("blocking", "metrics", f"{key} is marked unavailable without {', '.join(missing)}", owner,
                    f"{key}: why can't it be computed here, and where does it live?")] if missing else []
    gaps = []
    missing = [f for f in METRIC_REQUIRED if f not in entry or entry.get(f) in (None, "")]
    if missing:
        gaps.append(gap("blocking", "metrics", f"{key} lacks {', '.join(missing)}", owner,
                        f"{key}: what are its {', '.join(missing)}?"))
    soft = [f for f in METRIC_RECOMMENDED if not entry.get(f)]
    if soft:
        gaps.append(gap("recommended", "metrics", f"{key} has no {', '.join(soft)}", owner,
                        f"{key}: {question_for(soft)}"))
    for part in ("numerator", "denominator"):
        value = entry.get(part)
        if isinstance(value, str) and re.search(r"\s", value.strip()) and not re.search(r"[()*/+\-=<>_.]", value):
            gaps.append(gap("recommended", "metrics", f"{key}: the {part} '{value}' reads like prose; ds-verify looks for "
                                                      "it in the readout's Metric line, so write the column or expression",
                            owner, f"{key}: which column or expression is the {part}?"))
    return gaps


def question_for(fields):
    asks = {"verified": "when and how was this definition last matched to the dashboard?",
            "pitfalls": "what do newcomers get wrong about it?",
            "aliases": "what other names do people use for it, in English and Chinese?"}
    return " ".join(asks[f] for f in fields)


# --- the data ------------------------------------------------------------------------------------------------

def table_columns(db, table):
    """Reference adapter: the columns of a SQLite table or view, or None when it doesn't exist."""
    conn = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
    try:
        rows = conn.execute(f'pragma table_info("{table}")').fetchall()
    finally:
        conn.close()
    return [r[1] for r in rows] or None


def audit_sources(metrics, db):
    gaps = []
    for key, entry in metrics.items():
        if not isinstance(entry, dict) or entry.get("available") is False or not entry.get("source"):
            continue
        columns = table_columns(db, entry["source"])
        if columns is None:
            gaps.append(gap("blocking", "data", f"{key}: its source {entry['source']} isn't in the database", entry.get("owner"),
                            f"{key}: which table or view is its source?"))
            continue
        named = [entry.get("numerator"), entry.get("denominator")] + list(entry.get("filters") or [])
        identifiers = {w for part in named if isinstance(part, str) for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", part)}
        unknown = sorted(w for w in identifiers if "_" in w and w not in columns)
        if unknown:
            gaps.append(gap("blocking", "data", f"{key}: {', '.join(unknown)} isn't a column of {entry['source']}",
                            entry.get("owner"), f"{key}: {', '.join(unknown)} isn't in {entry['source']}; what is the column now?"))
    return gaps


# --- the project ---------------------------------------------------------------------------------------------

def project_files(project):
    found, count = {"queries": [], "readouts": []}, 0
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            count += 1
            if count > MAX_FILES:
                return found
            path = os.path.join(root, name)
            if name in (".ds-queries.log", "queries.log"):
                found["queries"].append(path)
            elif name.endswith(".md") and name != "AGENTS.md":
                try:
                    head = open(path, encoding="utf-8", errors="replace").read(20000)
                except OSError:
                    continue
                if re.search(r"^#+\s*Answer", head, re.M) and METRIC_LINE.search(head):
                    found["readouts"].append((path, head))
    return found


def audit_project(project, metrics, tables):
    gaps = []
    agents = os.path.join(project, "AGENTS.md")
    if not os.path.exists(agents):
        gaps.append(gap("blocking", "playbook", f"{project} has no AGENTS.md, so Codex and Cursor won't load ds-mode"))
    else:
        text = open(agents, encoding="utf-8", errors="replace").read()
        for skill, severity in (("ds-mode", "blocking"), ("ds-verify", "recommended")):
            paths = re.findall(rf"(\S*{skill}/SKILL\.md)", text)
            if not paths:
                gaps.append(gap(severity, "playbook", f"AGENTS.md doesn't point to {skill}/SKILL.md"))
            elif not any(os.path.exists(os.path.expanduser(p)) for p in paths):
                gaps.append(gap("blocking", "playbook", f"AGENTS.md points to {paths[0]}, which doesn't exist"))
    found = project_files(project)
    used = {}
    for path in found["queries"]:
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                sql = json.loads(line).get("sql") or ""
            except (ValueError, AttributeError):
                continue
            for table in SQL_TABLE.findall(re.sub(r"'(?:[^']|'')*'", " ", sql)):
                if not table.lower().startswith(("scratch", "sqlite_", "pragma")):
                    used[table] = used.get(table, 0) + 1
    for table, count in sorted(used.items(), key=lambda kv: -kv[1]):
        entry = tables.get(table) if isinstance(tables, dict) else None
        missing = [f for f in TABLE_FIELDS if not (entry or {}).get(f)]
        if missing:
            owner = (entry or {}).get("owner")
            gaps.append(gap("recommended", "tables", f"{table} (in {count} logged queries) has no {', '.join(missing)} in tables.json",
                            owner, f"{table}: what are its {', '.join(missing)}? (complete_when: when is a day's data complete?)"))
    guessed, ignored = {}, {}
    for path, text in found["readouts"]:
        for definition in METRIC_LINE.findall(text):
            if not re.search(r"\[guess\]|stated here", definition, re.I) or "metrics.json" in definition.lower():
                continue
            own = re.sub(r",?\s*(?:from\s+)?stated here\s*(?:\[guess\])?|\[guess\]", "", definition, flags=re.I).strip(" ,`*")
            relpath = os.path.relpath(path, project)
            overlap = overlay_metric_for(own, metrics)
            if overlap:
                ignored.setdefault(overlap, []).append(relpath)
            else:
                # Group by the definition itself, without trailing notes ("conversions / searches, summed over 7 days").
                core = re.split(r"[,，;；]|\s\(", own, maxsplit=1)[0]
                guessed.setdefault(re.sub(r"\s+", " ", core.lower()).strip()[:100], []).append(relpath)
    for key, paths in sorted(ignored.items()):
        gaps.append(gap("recommended", "playbook", f"metrics.json defines {key}, but {len(paths)} readout(s) wrote their own "
                                                   f"definition from the same columns (e.g. {paths[0]}): check that DS_OVERLAY_DIR "
                                                   "was set and AGENTS.md pointed to ds-mode when they ran"))
    for own, paths in sorted(guessed.items(), key=lambda kv: -len(kv[1])):
        gaps.append(gap("blocking" if len(paths) >= 2 else "recommended", "metrics",
                        f"{len(paths)} readout(s) defined a metric that metrics.json lacks, themselves ([guess]): '{own}' "
                        f"(e.g. {paths[0]})", None,
                        f"Readouts defined a metric as '{own}'. Which team metric is it, and what is its definition "
                        "(numerator, denominator, filters, grain, source, owner)?"))
    return gaps, {"tables_used": used, "readouts": len(found["readouts"]), "query_logs": len(found["queries"])}


def identifiers(text):
    return {w.lower() for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", str(text)) if "_" in w}


def overlay_metric_for(definition, metrics):
    """The overlay metric whose numerator or denominator columns the agent's own definition uses, if any."""
    used = identifiers(definition)
    for key, entry in metrics.items():
        if not isinstance(entry, dict):
            continue
        columns = identifiers(entry.get("numerator")) | identifiers(entry.get("denominator"))
        names = {key.lower()} | {a.lower() for a in entry.get("aliases", []) if isinstance(a, str)}
        if used & columns or any(re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])", definition.lower()) for n in names):
            return key
    return None


# --- the questionnaires --------------------------------------------------------------------------------------

def write_questions(gaps, out):
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, ".gitignore"), "w") as handle:
        handle.write("# Questions name internal metrics and tables; keep them out of git.\n*\n")
    by_owner = {}
    for item in gaps:
        if item["question"]:
            by_owner.setdefault(item["owner"] or "unknown owner", []).append(item)
    written = []
    for owner, items in sorted(by_owner.items()):
        slug = re.sub(r"[^A-Za-z0-9]+", "-", owner).strip("-").lower() or "owner"
        path = os.path.join(out, f"questions-{slug}.md")
        lines = [f"# Questions for {owner}", "",
                 "ds-stack's agents read the team's definitions from a private file. These answers go into it, written "
                 "by a person on the team; the agent never fills them in.", ""]
        for i, item in enumerate(sorted(items, key=lambda x: x["severity"] != "blocking"), 1):
            tag = "needed" if item["severity"] == "blocking" else "helps"
            lines.append(f"{i}. ({tag}) {item['question']}")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
        written.append(path)
    return written


def render(report):
    blocking = [g for g in report["gaps"] if g["severity"] == "blocking"]
    recommended = [g for g in report["gaps"] if g["severity"] == "recommended"]
    usage = report["usage"]
    lines = [f"ds-ready: {'not ready' if blocking else 'ready'} ({len(blocking)} blocking, {len(recommended)} recommended; "
             f"read {usage['query_logs']} query logs and {usage['readouts']} readouts)"]
    for title, items in (("Blocking", blocking), ("Recommended", recommended)):
        if items:
            lines.append(f"{title}:")
            lines += [f"  - [{g['area']}] {g['message']}" for g in items]
    if report["questions"]:
        lines.append("Questions for the owners (send them; a person writes the answers into the overlay):")
        lines += [f"  {path}" for path in report["questions"]]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--overlay", default=os.environ.get("DS_OVERLAY_DIR"))
    parser.add_argument("--project", default=".")
    parser.add_argument("--db", default=os.environ.get("DS_WAREHOUSE"), help="SQLite file to check sources against")
    parser.add_argument("--out", default="ds-ready", help="where the questionnaires go")
    parser.add_argument("--json", help="also write the report as JSON")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.project):
        print(f"ds-ready: no project folder at {args.project}", file=sys.stderr)
        return 3
    gaps, metrics, tables = audit_overlay(args.overlay)
    if args.db and metrics:
        if os.path.exists(args.db):
            gaps += audit_sources(metrics, args.db)
        else:
            gaps.append(gap("recommended", "data", f"no database at {args.db}, so sources weren't checked"))
    project_gaps, usage = audit_project(args.project, metrics, tables)
    gaps += project_gaps
    report = {"gaps": gaps, "usage": usage, "questions": write_questions(gaps, args.out)}
    print(render(report))
    if args.json:
        with open(args.json, "w") as handle:
            json.dump(report, handle, indent=2, default=str)
    return 1 if any(g["severity"] == "blocking" for g in gaps) else 0


if __name__ == "__main__":
    sys.exit(main())
