#!/usr/bin/env python3
"""Audit a work project for what ds-stack needs, list the gaps, and write questions for the metric owners.

    python3 tools/audit.py [--project DIR] [--overlay DIR] [--db FILE] [--out DIR] [--json report.json]

It reads, and never writes, the overlay (--overlay, else $DS_OVERLAY_DIR): metrics.json, tables.json,
runner.json, reviewers.json and denylist.txt. It reads the project folder (default: the current one): its
AGENTS.md, and the query logs and readouts of past analyses under it, to see which tables and metrics the work
actually uses. With --db (else $DS_WAREHOUSE) it checks each metric's source table and columns (SQLite
reference; a warehouse port replaces table_columns()).

Each gap is "blocking" (ds-mode can't be trusted on this project until it is fixed) or "recommended". For each
metric owner it writes <out>/questions-<owner>.md (default <project>/ds-ready). It refuses an --out that holds
anything else, and adds a .gitignore only to a folder it created. --json goes wherever you point it, outside
that .gitignore. Metric definitions are a person's to write: the audit asks, it never drafts one.

Exit code: 0 no blocking gap, 1 at least one, 3 usage or internal error.
"""

import argparse
import json
import os
import re
import sqlite3
import sys

STRING_FIELDS = ("numerator", "denominator", "grain", "source", "owner")
METRIC_RECOMMENDED = ("verified", "pitfalls", "aliases")
TABLE_FIELDS = ("grain", "keys", "complete_when", "owner", "pitfalls")
METRIC_LINE = re.compile(r"^\s*[-*]?\s*(?:metric|指标)\s*[:：]\s*(.+)$", re.I | re.M)
GUESS = re.compile(r"\[guess\]|stated here", re.I)
FROM_OVERLAY = re.compile(r"from\s+(?:the\s+)?`?metrics\.json|来自\s*`?metrics\.json", re.I)
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "ds-ready", "ds-interrogate", "ds-retro",
             ".ipynb_checkpoints", ".cache", ".mypy_cache", ".pytest_cache", "dist", "build", "site-packages"}
SQL_WORDS = {"and", "or", "not", "in", "is", "null", "like", "case", "when", "then", "else", "end", "interval",
             "day", "days", "between", "as", "distinct", "true", "false", "select", "from", "where"}
DEFINITION_STOPWORDS = SQL_WORDS | {"sum", "count", "avg", "min", "max", "stated", "here", "guess", "there", "no",
                                    "metrics", "json", "over", "the", "per", "of", "week", "weekly", "daily", "all",
                                    "summed", "total", "a", "an", "for", "with", "by", "to", "on", "at", "only"}


def gap(severity, area, message, owner=None, question=None):
    return {"severity": severity, "area": area, "message": message,
            "owner": str(owner) if owner not in (None, "") else None, "question": question}


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


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
            metrics = json.loads(read_text(path))
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
            loaded = json.loads(read_text(tables_path))
            tables = loaded if isinstance(loaded, dict) else {}
        except ValueError as err:
            gaps.append(gap("blocking", "tables", f"tables.json isn't valid JSON: {err}"))
    for name, why in (("runner.json", "the query runner uses its defaults"),
                      ("reviewers.json", "ds-interrogate uses Codex and Claude Code by default; list the CLIs approved "
                                         "for company data"),
                      ("denylist.txt", "the commit hooks block every commit until it exists")):
        if not os.path.exists(os.path.join(overlay, name)):
            gaps.append(gap("recommended", "overlay", f"{name} is missing: {why}"))
    denylist = os.path.join(overlay, "denylist.txt")
    if os.path.exists(denylist) and not [l for l in read_text(denylist).splitlines() if l.strip() and not l.startswith("#")]:
        gaps.append(gap("recommended", "overlay", "denylist.txt lists no term: add codenames and internal table names"))
    return gaps, metrics, tables


def audit_metric(key, entry):
    if not isinstance(entry, dict):
        return [gap("blocking", "metrics", f"{key}: the entry isn't an object")]
    owner = entry.get("owner")
    if "available" in entry and not isinstance(entry["available"], bool):
        return [gap("blocking", "metrics", f"{key}: available must be the JSON value true or false, not "
                                           f"{json.dumps(entry['available'])}", owner)]
    if entry.get("available") is False:
        missing = [f for f in ("note", "owner") if not (isinstance(entry.get(f), str) and entry[f].strip())]
        return [gap("blocking", "metrics", f"{key} is marked unavailable without {', '.join(missing)}", owner,
                    f"{key}: why can't it be computed here, and where does it live?")] if missing else []
    gaps = []
    order = ("numerator", "denominator", "filters", "grain", "source", "owner")
    missing = [f for f in order if f not in entry]
    wrong = [f for f in STRING_FIELDS if f in entry and not (isinstance(entry[f], str) and entry[f].strip())]
    filters = entry.get("filters")
    if "filters" in entry and not (isinstance(filters, list) and all(isinstance(f, str) and f.strip() for f in filters)):
        wrong.append("filters (a list of strings)")
    if missing:
        gaps.append(gap("blocking", "metrics", f"{key} lacks {', '.join(missing)}", owner, f"{key}: what are its {', '.join(missing)}?"))
    if wrong:
        gaps.append(gap("blocking", "metrics", f"{key} has an empty or wrongly typed {', '.join(wrong)}", owner,
                        f"{key}: what are its {', '.join(f.split(' ')[0] for f in wrong)}?"))
    soft = [f for f in METRIC_RECOMMENDED if not entry.get(f)]
    badly_typed = [f for f in ("pitfalls", "aliases") if entry.get(f) and not
                   (isinstance(entry[f], list) and all(isinstance(x, str) for x in entry[f]))]
    if soft:
        gaps.append(gap("recommended", "metrics", f"{key} has no {', '.join(soft)}", owner, f"{key}: {question_for(soft)}"))
    if badly_typed:
        gaps.append(gap("recommended", "metrics", f"{key}: {', '.join(badly_typed)} should be a list of strings", owner))
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
    """Reference adapter: the lowercased columns of a SQLite table or view, or None when it doesn't exist.
    A schema prefix (main.search_daily) is dropped. Raises sqlite3.Error when db isn't a SQLite file."""
    name = table.split(".")[-1].strip('"`[]')
    conn = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
    try:
        rows = conn.execute(f'pragma table_info("{name}")').fetchall()
    finally:
        conn.close()
    return [r[1].lower() for r in rows] or None


def expression_identifiers(expression):
    """Column-like names in an expression: no string literals, no function names, no SQL words."""
    bare = re.sub(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"", " ", str(expression))
    names = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b(?!\s*\()", bare)
    return {n.lower() for n in names if n.lower() not in SQL_WORDS}


def audit_sources(metrics, db):
    gaps = []
    for key, entry in metrics.items():
        if not isinstance(entry, dict) or entry.get("available") is False or not isinstance(entry.get("source"), str):
            continue
        try:
            columns = table_columns(db, entry["source"])
        except sqlite3.Error as err:
            return gaps + [gap("blocking", "data", f"{db} can't be read as a SQLite database ({err}); pass the database "
                                                   "the agent queries, or a warehouse adapter")]
        owner = entry.get("owner")
        if columns is None:
            gaps.append(gap("blocking", "data", f"{key}: its source {entry['source']} isn't in the database", owner,
                            f"{key}: which table or view is its source?"))
            continue
        core = [p for p in (entry.get("numerator"), entry.get("denominator")) if isinstance(p, str)]
        unknown = sorted(n for p in core for n in expression_identifiers(p) if n not in columns)
        if unknown:
            gaps.append(gap("blocking", "data", f"{key}: {', '.join(unknown)} isn't a column of {entry['source']}", owner,
                            f"{key}: {', '.join(unknown)} isn't in {entry['source']}; what is the column now?"))
        filters = [f for f in entry.get("filters") or [] if isinstance(f, str)]
        loose = sorted(n for f in filters for n in expression_identifiers(f) if n not in columns)
        if loose:
            gaps.append(gap("recommended", "data", f"{key}: the filters name {', '.join(loose)}, which isn't a column of "
                                                   f"{entry['source']}; quote it if it is a value", owner))
    return gaps


# --- the project ---------------------------------------------------------------------------------------------

def project_files(project, max_files):
    found, seen = {"queries": [], "readouts": [], "truncated": False}, 0
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not (name in (".ds-queries.log", "queries.log") or (name.endswith(".md") and name != "AGENTS.md")):
                continue
            seen += 1
            if seen > max_files:
                found["truncated"] = True
                return found
            path = os.path.join(root, name)
            if name.endswith(".log"):
                found["queries"].append(path)
                continue
            try:
                head = read_text(path)[:20000]
            except OSError:
                continue
            if re.search(r"^#+\s*Answer", head, re.M) and METRIC_LINE.search(head):
                found["readouts"].append((path, head))
    return found


def skill_paths(text, skill, project):
    """Paths to <skill>/SKILL.md named in AGENTS.md outside comments, resolved; (written, resolved) pairs."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"[`\[\]()<>]", " ", text)
    pairs = []
    for written in re.findall(rf"([~$A-Za-z0-9_./{{}}-]*{re.escape(skill)}/SKILL\.md)", text):
        resolved = os.path.expandvars(os.path.expanduser(written))
        if not os.path.isabs(resolved):
            resolved = os.path.join(project, resolved)
        pairs.append((written, resolved))
    return pairs


def audit_agents(project):
    agents = os.path.join(project, "AGENTS.md")
    if not os.path.exists(agents):
        return [gap("blocking", "playbook", f"{project} has no AGENTS.md, so Codex and Cursor won't load ds-mode")]
    gaps = []
    text = read_text(agents)
    for skill, severity in (("ds-mode", "blocking"), ("ds-verify", "recommended")):
        pairs = skill_paths(text, skill, project)
        if not pairs:
            gaps.append(gap(severity, "playbook", f"AGENTS.md doesn't point to {skill}/SKILL.md"))
        elif not any(os.path.exists(resolved) for _, resolved in pairs):
            gaps.append(gap(severity, "playbook", f"AGENTS.md points to {pairs[0][0]}, which doesn't exist"))
    return gaps


def tables_in(sql):
    """Data tables a query reads: no comments, literals, CTE names, function arguments or system catalogs."""
    sql = re.sub(r"--[^\n]*|/\*.*?\*/", " ", str(sql), flags=re.S)
    sql = re.sub(r"'(?:[^']|'')*'", " ", sql)
    sql = re.sub(r"\b(?:extract|substring|substr|trim|position|overlay)\s*\([^()]*\)", " ", sql, flags=re.I)
    ctes = {c.lower() for c in re.findall(r"(?:\bwith\s+(?:recursive\s+)?|,\s*)([A-Za-z_]\w*)\s+as\s*\(", sql, re.I)}
    names = set()
    for table in re.findall(r"\b(?:from|join)\s+([A-Za-z_][\w.]*)", sql, re.I):
        bare = table.lower().split(".")[-1]
        if bare in ctes or table.lower().startswith(("information_schema", "sqlite_", "pg_catalog")) or bare.startswith("scratch"):
            continue
        names.add(bare)
    return names


def definition_key(definition):
    """The columns an agent's own definition uses, so different wordings of one metric group together."""
    right = definition.split("=", 1)[1] if "=" in definition else definition
    right = re.sub(r"（[^）]*）|\[guess\]|stated here.*$", " ", right, flags=re.I)  # full-width notes only; sum(x) keeps x
    words = {w.lower().rstrip("s") for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", right)}
    return tuple(sorted(w for w in words if w not in DEFINITION_STOPWORDS and len(w) > 2))


def identifiers(text):
    return {w.lower() for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", str(text)) if "_" in w}


def overlay_metric_for(definition, metrics):
    """The overlay metric whose numerator or denominator columns the agent's own definition uses, if any."""
    used = identifiers(definition)
    for key, entry in metrics.items():
        if not isinstance(entry, dict):
            continue
        columns = set()
        for part in (entry.get("numerator"), entry.get("denominator")):
            if isinstance(part, str):
                columns |= identifiers(part)
        names = {key.lower()} | {a.lower() for a in (entry.get("aliases") or []) if isinstance(a, str)}
        if used & columns or any(re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])", definition.lower()) for n in names):
            return key
    return None


def audit_project(project, metrics, tables, max_files):
    gaps = audit_agents(project)
    found = project_files(project, max_files)
    if found["truncated"]:
        gaps.append(gap("blocking", "project", f"the scan stopped after {max_files} readouts and logs under {project}, so "
                                               "some were missed; point --project at the analyses or raise --max-files"))
    used = {}
    for path in found["queries"]:
        for line in read_text(path).splitlines():
            try:
                sql = json.loads(line).get("sql") or ""
            except (ValueError, AttributeError):
                continue
            for table in tables_in(sql):
                used[table] = used.get(table, 0) + 1
    notes = {str(k).lower().split(".")[-1]: v for k, v in (tables or {}).items()}
    for table, count in sorted(used.items(), key=lambda kv: -kv[1]):
        entry = notes.get(table) if isinstance(notes.get(table), dict) else {}
        missing = [f for f in TABLE_FIELDS if not entry.get(f)]
        if missing:
            gaps.append(gap("recommended", "tables", f"{table} (in {count} logged queries) has no {', '.join(missing)} in "
                                                     "tables.json", entry.get("owner"),
                            f"{table}: what are its {', '.join(missing)}? (complete_when: when is a day's data complete?)"))
    guessed, ignored = {}, {}
    for path, text in found["readouts"]:
        for definition in METRIC_LINE.findall(text):
            if not GUESS.search(definition):
                continue  # taken from metrics.json, or not marked as the agent's own
            if FROM_OVERLAY.search(definition) and not re.search(r"\[guess\]", definition, re.I):
                continue
            relpath = os.path.relpath(path, project)
            own = re.split(r"\s*(?:,\s*)?(?:from\s+)?stated here", definition, maxsplit=1, flags=re.I)[0].strip(" ,`*")
            overlap = overlay_metric_for(own, metrics)
            if overlap:
                ignored.setdefault(overlap, []).append(relpath)
            else:
                group = guessed.setdefault(definition_key(own) or (own.lower()[:60],), {"examples": [], "paths": []})
                group["paths"].append(relpath)
                group["examples"].append(own[:80])
    for key, paths in sorted(ignored.items()):
        gaps.append(gap("recommended", "playbook", f"metrics.json defines {key}, but {len(paths)} readout(s) wrote their own "
                                                   f"definition from the same columns (e.g. {paths[0]}): check that DS_OVERLAY_DIR "
                                                   "was set and AGENTS.md pointed to ds-mode when they ran"))
    for _, group in sorted(guessed.items(), key=lambda kv: -len(kv[1]["paths"])):
        paths, own = group["paths"], group["examples"][0]
        gaps.append(gap("blocking" if len(paths) >= 2 else "recommended", "metrics",
                        f"{len(paths)} readout(s) defined a metric that metrics.json lacks, themselves ([guess]): '{own}' "
                        f"(e.g. {paths[0]})", None,
                        f"Readouts defined a metric as '{own}'. Which team metric is it, and what is its definition "
                        "(numerator, denominator, filters, grain, source, owner)?"))
    return gaps, {"tables_used": used, "readouts": len(found["readouts"]), "query_logs": len(found["queries"]),
                  "truncated": found["truncated"]}


# --- the questionnaires --------------------------------------------------------------------------------------

def prepare_out(out):
    """Create the questions folder, or reuse one that holds only earlier questions. Refuse anything else."""
    if os.path.exists(out):
        others = [n for n in os.listdir(out) if not (n == ".gitignore" or re.fullmatch(r"questions-.+\.md", n))]
        if others:
            raise ValueError(f"{out} holds other files ({', '.join(sorted(others)[:3])}); pick an empty or new --out")
        for name in os.listdir(out):
            if name.startswith("questions-"):
                os.remove(os.path.join(out, name))
        return
    os.makedirs(out)
    with open(os.path.join(out, ".gitignore"), "w") as handle:
        handle.write("# Questions name internal metrics and tables; keep them out of git.\n*\n")


def write_questions(gaps, out):
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
            lines.append(f"{i}. ({'needed' if item['severity'] == 'blocking' else 'helps'}) {item['question']}")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
        written.append(path)
    return written


def render(report):
    blocking = [g for g in report["gaps"] if g["severity"] == "blocking"]
    recommended = [g for g in report["gaps"] if g["severity"] == "recommended"]
    usage = report["usage"]
    lines = [f"ds-ready: {'not ready' if blocking else 'ready'} ({len(blocking)} blocking, {len(recommended)} recommended; "
             f"read {usage['query_logs']} query logs and {usage['readouts']} readouts"
             + ("; the scan was cut short" if usage.get("truncated") else "") + ")"]
    for title, items in (("Blocking", blocking), ("Recommended", recommended)):
        if items:
            lines.append(f"{title}:")
            lines += [f"  - [{g['area']}] {g['message']}" for g in items]
    if report["questions"]:
        lines.append("Questions for the owners (send them; a person writes the answers into the overlay):")
        lines += [f"  {path}" for path in report["questions"]]
    return "\n".join(lines)


def run(args):
    if not os.path.isdir(args.project):
        print(f"ds-ready: no project folder at {args.project}", file=sys.stderr)
        return 3
    out = args.out or os.path.join(args.project, "ds-ready")
    try:
        prepare_out(out)
    except ValueError as err:
        print(f"ds-ready: {err}", file=sys.stderr)
        return 3
    gaps, metrics, tables = audit_overlay(args.overlay)
    if args.db and metrics:
        if os.path.exists(args.db):
            gaps += audit_sources(metrics, args.db)
        else:
            gaps.append(gap("recommended", "data", f"no database at {args.db}, so sources weren't checked"))
    project_gaps, usage = audit_project(args.project, metrics, tables, args.max_files)
    gaps += project_gaps
    report = {"gaps": gaps, "usage": usage, "questions": write_questions(gaps, out)}
    print(render(report))
    if args.json:
        with open(args.json, "w") as handle:
            json.dump(report, handle, indent=2, default=str)
    return 1 if any(g["severity"] == "blocking" for g in gaps) else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--overlay", default=os.environ.get("DS_OVERLAY_DIR"))
    parser.add_argument("--project", default=".")
    parser.add_argument("--db", default=os.environ.get("DS_WAREHOUSE"), help="SQLite file to check sources against")
    parser.add_argument("--out", help="where the questionnaires go (default: <project>/ds-ready)")
    parser.add_argument("--max-files", type=int, default=5000, help="readouts and query logs to read before stopping")
    parser.add_argument("--json", help="also write the report as JSON (not covered by the .gitignore)")
    args = parser.parse_args(argv)
    try:
        return run(args)
    except Exception as err:  # noqa: BLE001 - a crash must not read as "not ready"
        print(f"ds-ready: internal error: {type(err).__name__}: {err}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
