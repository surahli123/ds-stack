#!/usr/bin/env python3
"""Sanitize work material so it can be shared to improve the generic skill.

    python3 sanitize.py FILE... --out-dir sanitized/ [--names names.txt] [--scale-lifts]

Run it on the work laptop with DS_OVERLAY_DIR set. The key that maps real names to
tokens (sanitize_key.json) stays in the overlay and is reused, so tokens stay stable
across runs. It is never written to the output folder.

Handles Statsig pulse responses, the pulse request (request.json), experiment configs
and audit logs; normalize.py's scorecard.json and config.json; prereg.json,
standards.json, evidence.json and daily series; CSV exports; text and Markdown
(readouts, triage notes, docs). Other JSON is scrubbed field by field.

What it keeps, changes and removes:
- Names become tokens: metrics (with their family when the pattern library or the
  overlay's metric_families.json knows it, so "success_metric_1" still reads as a
  success metric), experiments, groups, layers, gates, parameters and their values,
  segments, and every line of --names (features, teams, products).
- Kept exactly by default: relative changes, their intervals, p-values, bars and
  margins, allocation percentages, analysis settings. The call and the deep dive
  compare them with fixed thresholds, and without names or dates they identify little.
  --scale-lifts multiplies all of them by one hidden factor (0.6 to 1.6). Signs and
  significance hold; comparisons with the family bands in search_patterns.json don't.
- Changed: means (each metric by its own hidden factor; absolute changes follow, so
  relative x control = absolute still holds); unit and exposure counts (scaled so the
  sample-split test gives the same p-value when the config is included); dates (moved
  by whole weeks, so weekdays hold).
- Removed: descriptions, owners, tags, links, emails, URLs, IP addresses, long IDs and
  handles. In text, money, counts and numbers of 100 or more become random digits of
  the same shape. CSV keeps its header and cell formats only, with random digits; for
  the numbers, normalize the CSV first and sanitize the scorecard.json.
- Free text (hypotheses, change logs, explanations, notes) is kept after scrubbing,
  because the deep dive reads it. Read it.
- Every output is checked against the denylist. If a term survives, nothing is written,
  and the files and terms are named on this screen only.

Read every output before sending it. This removes what it recognises, not everything.
"""

import argparse
import copy
import csv
import io
import json
import math
import os
import random
import re
import sys
from datetime import date, datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import explain  # noqa: E402
from decide import _key as name_key  # noqa: E402  the same matching decide.py uses ('Latency P95 ms' = 'Latency p95 (ms)')

SCRUB = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "<email>"),
         (re.compile(r"\b(?:https?://|www\.)\S+"), "<url>"),
         (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "<ip>"),
         (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "<id>"),
         (re.compile(r"\b(?=[0-9a-f]*\d)[0-9a-f]{16,}\b", re.I), "<id>"),
         (re.compile(r"(?<![\w<])@[A-Za-z][\w.-]{2,}"), "<handle>")]
DROP_KEYS = {"description", "creatorName", "creatorEmail", "creatorID", "lastModifierName", "lastModifierEmail",
             "lastModifierID", "ownerName", "ownerEmail", "ownerID", "team", "tags", "links", "targetApps",
             "modifierEmail", "modifierName", "modifierID", "updatedBy", "updatedByUserID", "experimentCreator",
             "experimentTeam", "experimentTags", "metricTags", "metricTeam", "owner", "reviewers", "url", "link"}
FREE_TEXT = {"hypothesis", "changeLog", "summary", "cause", "evidence", "reason", "notes", "note", "comment",
             "rationale", "source", "_note", "message", "title", "decisionReason"}
GENERIC = {"", "true", "false", "on", "off", "yes", "no", "none", "null", "enabled", "disabled", "control", "test",
           "treatment", "default", "baseline", "increase", "decrease", "primary", "secondary", "guardrail", "monitoring",
           "ratio", "mean", "sum", "count", "event_count", "event_user", "user_count", "funnel", "pass", "fail",
           "passed", "failed", "warning", "significant", "not significant", "n/a", "na", "-"}
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DATES = re.compile(r"(?P<iso>\b\d{4}-\d{2}-\d{2})"
                   r"|(?P<slash>\b\d{1,2}/\d{1,2}/(?:\d{4}|\d{2})\b)"
                   r"|(?P<mon>\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.? \d{1,2}\b(?:, \d{4})?)", re.I)
NUMBER = re.compile(r"(?<![\w.])(?P<cur>[$€£¥])?(?P<n>\d[\d,]*(?:\.\d+)?)(?P<suf>%|\s?pp\b|\s?bps\b|[kKmMbB]\b)?")


class Key:
    """The mapping from real names to tokens, and the hidden factors. Stays on the work machine."""

    def __init__(self, path, library=None, seed=None, scale_lifts=False):
        self.path = path
        data = {}
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
        rng = random.Random(seed) if seed is not None else random.SystemRandom()
        self.rng = rng
        self.strings = data.get("strings", {})
        self.counters = data.get("counters", {})
        self.factors = data.get("factors", {})
        self.date_shift = data.get("date_shift_days") or -7 * rng.randint(9, 57)
        self.text_seed = data.get("text_seed") or rng.randint(1, 10 ** 9)
        self.library = library or {"families": {}}
        self.exact = {str(n).lower(): f for f, names in self.library.get("exact_families", {}).items()
                      for n in (names if isinstance(names, list) else [names])}
        self.k = self.factor("lift", 0.6, 1.6) if scale_lifts else 1.0
        self.keep = {str(v).lower() for dim, values in self.library.get("segment_dimensions", {}).items()
                     for v in [dim] + list(values)}
        self._regex = None
        self.reshaped = {}

    # ----- names -----
    def family(self, name, direction=None):
        if name.lower() in self.exact:
            return self.exact[name.lower()]
        found = explain.family_candidates(self.library, {"metric": name, "directionality": direction})
        return found[0] if len(found) == 1 else None

    def token(self, kind, real, direction=None):
        if real is None or isinstance(real, (bool, int, float)):
            return real
        real = str(real)
        if real.strip().lower() in GENERIC or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", real.strip()):
            return real
        if real in self.strings:
            return self.strings[real]
        if real in set(self.strings.values()):
            return real  # already a token
        if kind in ("segment", "dimension") and real.strip().lower() in self.keep:
            return real  # generic search vocabulary (device, query class, intent ...), see search_patterns.json
        for known, token in self.strings.items():
            same_kind = re.fullmatch(r"(\w+_)?metric_\d+", token) if kind == "metric" else token.startswith(f"{kind}_")
            if same_kind and name_key(known) == name_key(real):
                self.strings[real] = token  # remember the spelling, so text using it is replaced too
                self._regex = None
                return token
        prefix = kind
        if kind == "metric":
            family = self.family(real, direction)
            prefix = f"{family}_metric" if family else "metric"
        elif kind == "param" and re.search(self.library.get("presentation_params", "$^"), real, re.I):
            prefix = "presentation_param"
        n = self.counters.get(prefix, 0) + 1
        self.counters[prefix] = n
        self.strings[real] = f"{prefix}_{n}"
        self._regex = None
        return self.strings[real]

    def metric(self, name, direction=None):
        """A metric name, keeping Statsig's '::type' suffix and canonical ' - segment' suffix."""
        if not isinstance(name, str):
            return name
        base, sep, kind = name.partition("::")
        if sep:
            return f"{self.metric(base, direction)}::{kind}"
        base, sep, seg = name.partition(" - ")
        if sep:
            return f"{self.token('metric', base, direction)} - {self.token('segment', seg)}"
        return self.token("metric", name, direction)

    def names(self):
        if self._regex is None:
            reals = sorted((s for s in self.strings if len(s) >= 3), key=len, reverse=True)
            self._lower = {s.lower(): self.strings[s] for s in reversed(reals)}
            self._regex = re.compile(r"(?<!\w)(" + "|".join(map(re.escape, reals)) + r")(?!\w)", re.I) if reals else None
        return self._regex

    def replace_names(self, text):
        regex = self.names()
        return regex.sub(lambda m: self._lower[m.group(1).lower()], text) if regex else text

    # ----- factors -----
    def factor(self, name, low, high):
        if name not in self.factors:
            self.factors[name] = round(self.rng.uniform(low, high), 6)
        return self.factors[name]

    def mean_factor(self, metric, control_mean=None):
        high = 2.0
        if control_mean is not None and 0 < control_mean < 1:
            high = max(0.55, min(2.0, 0.98 / control_mean))  # a rate stays below 1
        return self.factor(f"mean:{metric}", 0.5, high)

    def save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump({"strings": self.strings, "counters": self.counters, "factors": self.factors,
                       "date_shift_days": self.date_shift, "text_seed": self.text_seed}, handle, indent=1)

    def families_out(self):
        out = {}
        for real, token in self.strings.items():
            match = re.fullmatch(r"(\w+)_metric_\d+", token)
            if match and match.group(1) in self.library["families"]:
                out.setdefault(match.group(1), []).append(token)
        return out


# ---------- text ----------

def shift_date(value, days):
    try:
        return (date.fromisoformat(value[:10]) + timedelta(days=days)).isoformat() + value[10:]
    except ValueError:
        return value


def shift_epoch(value, days):
    ms = value > 1e11
    shifted = datetime.fromtimestamp(value / 1000 if ms else value, tz=timezone.utc) + timedelta(days=days)
    return int(shifted.timestamp() * (1000 if ms else 1))


def _shift_match(m, days):
    text = m.group(0)
    try:
        if m.group("iso"):
            return shift_date(text, days)
        if m.group("slash"):
            mo, d, y = (int(x) for x in text.split("/"))
            y = y + 2000 if y < 100 else y
            new = date(y, mo, d) + timedelta(days=days)
            return f"{new.month}/{new.day}/{new.year if len(text.split('/')[2]) == 4 else str(new.year)[2:]}"
        words = re.match(r"([a-z]+)\.? (\d{1,2})(?:, (\d{4}))?", text, re.I)
        month = MONTHS.index(words.group(1)[:3].lower()) + 1
        new = date(int(words.group(3) or 2001), month, int(words.group(2))) + timedelta(days=days)
        out = f"{MONTHS[new.month - 1].title()} {new.day}"
        return out + (f", {new.year}" if words.group(3) else "")
    except (ValueError, AttributeError):
        return text


def _reshape(digits, rng):
    """Random digits of the same shape. Leading zeros stay, so 0.004 stays 0.00x and the magnitude holds."""
    out, leading = [], True
    for ch in digits:
        if ch.isdigit() and leading and ch == "0":
            out.append(ch)
        elif ch.isdigit():
            out.append(str(rng.randint(1, 9) if leading else rng.randint(0, 9)))
            leading = False
        else:
            out.append(ch)
    return "".join(out)


def scrub_numbers(text, key, strict):
    rng = random.Random(key.text_seed + len(key.reshaped))

    def one(m):
        if m.start() > 0 and text[m.start() - 1] == "_":
            return m.group(0)
        n, cur, suf = m.group("n"), m.group("cur"), (m.group("suf") or "").strip()
        plain = n.replace(",", "")
        is_year = re.fullmatch(r"(19|20)\d\d", n) is not None
        small = not cur and suf not in ("k", "K", "m", "M", "b", "B") and "," not in n and float(plain) < 100
        if is_year or (not strict and (suf in ("%", "pp", "bps") or small)):
            return m.group(0)
        if n not in key.reshaped:
            key.reshaped[n] = _reshape(n, rng)
        return m.group(0).replace(n, key.reshaped[n], 1)

    return NUMBER.sub(one, text)


def scrub_text(text, key, strict=False):
    """Free text: patterns, then names, then dates, then numbers."""
    if not isinstance(text, str):
        return text
    for pattern, placeholder in SCRUB:
        text = pattern.sub(placeholder, text)
    text = key.replace_names(text)
    pieces, last = [], 0
    for m in DATES.finditer(text):
        pieces.append(scrub_numbers(text[last:m.start()], key, strict))
        pieces.append(_shift_match(m, key.date_shift))
        last = m.end()
    pieces.append(scrub_numbers(text[last:], key, strict))
    return "".join(pieces)


def scrub_string(value, key):
    """A structured string: patterns and names; a whole-string date is shifted."""
    for pattern, placeholder in SCRUB:
        value = pattern.sub(placeholder, value)
    value = key.replace_names(value)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:[T ][\w:.+-]*)?", value):
        value = shift_date(value, key.date_shift)
    return value


def walk(obj, key, strict=False, numbers=False):
    """Scrub every string in a JSON value. Free-text fields get the full text treatment."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in DROP_KEYS:
                continue
            new_k = scrub_string(k, key) if isinstance(k, str) else k
            out[new_k] = scrub_text(v, key, strict) if k in FREE_TEXT and isinstance(v, str) else walk(v, key, strict, numbers)
        return out
    if isinstance(obj, list):
        return [walk(v, key, strict, numbers) for v in obj]
    if isinstance(obj, str):
        return scrub_string(obj, key)
    if numbers and isinstance(obj, (int, float)) and not isinstance(obj, bool):
        new = scrub_numbers(repr(obj) if isinstance(obj, float) else str(obj), key, strict)
        try:
            return type(obj)(new)
        except ValueError:
            return obj
    return obj


# ---------- counts ----------

def scale_counts(counts, shares, u):
    """Scale counts by u so the chi-square sample-split statistic is unchanged.

    For expected share q_g and n = sum: new_g = u*n*q_g + (count_g - n*q_g)*sqrt(u).
    Without shares the counts are scaled plainly (the split can't be tested anyway)."""
    if not counts:
        return counts
    n = sum(counts)
    if not shares or len(shares) != len(counts) or n <= 0:
        return [int(round(c * u)) for c in counts]
    total = sum(shares)
    out = [u * n * s / total + (c - n * s / total) * math.sqrt(u) for c, s in zip(counts, shares)]
    rounded = [max(0, int(round(x))) for x in out]
    rounded[-1] = max(0, int(round(u * n)) - sum(rounded[:-1]))
    return rounded


class Context:
    """What the handlers share: the key, the lift factor, the unit factor and the planned split."""

    def __init__(self, key):
        self.key = key
        self.k = key.k
        self.u = key.factor("units", 0.7, 1.4)
        self.sizes = {}          # group id or name (real) -> size percent
        self.control = None      # real control group id or name
        self.test = None         # real test group from request.json
        self.notes = []

    def pair_shares(self, test_group=None):
        """[control share, test share] for a pulse comparison, or None."""
        test_group = test_group or self.test
        control = self.sizes.get(self.control) or self.sizes.get("Control") or self.sizes.get("control")
        test = self.sizes.get(test_group)
        if test is None:
            others = {v for g, v in self.sizes.items() if g not in (self.control, "Control", "control")}
            test = others.pop() if len(others) == 1 else None
        return [control, test] if control and test else None


# ---------- Statsig ----------

def _scale_pulse_metric(m, ctx, shares):
    key, k = ctx.key, ctx.k
    m = dict(m)
    direction = m.get("directionality")
    real = None
    for name_key in ("metricID", "metricId", "metric_id"):
        if name_key in m:
            real = str(m[name_key]).partition("::")[0]
            m[name_key] = key.metric(str(m[name_key]), direction)
    if "metricName" in m:
        real = real or m["metricName"]
        m["metricName"] = key.metric(m["metricName"], direction)
    control = m.get("controlMean")
    s = key.mean_factor(real or "metric", control if isinstance(control, (int, float)) else None)
    if isinstance(control, (int, float)):
        m["controlMean"] = control * s
        if isinstance(m.get("testMean"), (int, float)):
            m["testMean"] = s * (control + k * (m["testMean"] - control))
    elif isinstance(m.get("testMean"), (int, float)):
        m["testMean"] *= s
    for f in ("percentChange", "percentConfidenceIntervalDelta", "percentSequentialTestingConfidenceIntervalDelta"):
        if isinstance(m.get(f), (int, float)):
            m[f] *= k
    for f in ("absoluteChange", "value", "absoluteConfidenceIntervalDelta", "confidenceIntervalDelta",
              "sequentialTestingConfidenceIntervalDelta", "testStd", "controlStd"):
        if isinstance(m.get(f), (int, float)):
            m[f] *= s * k
    for f, factor in (("percentConfidenceInterval", k), ("confidenceInterval", s * k), ("sequentialTestingConfidenceInterval", s * k)):
        bounds = m.get(f)
        if isinstance(bounds, dict) and {"lower", "upper"} <= set(bounds):
            m[f] = {b: v * factor if isinstance(v, (int, float)) else v for b, v in bounds.items()}
        elif isinstance(bounds, list) and len(bounds) == 2:
            m[f] = [b * factor if isinstance(b, (int, float)) else b for b in bounds]
    if isinstance(m.get("controlUnits"), (int, float)) and isinstance(m.get("testUnits"), (int, float)):
        m["controlUnits"], m["testUnits"] = scale_counts([m["controlUnits"], m["testUnits"]], shares, ctx.u)
    return m


def sanitize_pulse(doc, ctx):
    doc = copy.deepcopy(doc)
    data = doc.get("data", doc)
    test_group = doc.get("test") or data.get("test")
    shares = ctx.pair_shares(test_group)
    if shares is None:
        ctx.notes.append("a pulse file had no matching config groups, so its unit counts were scaled plainly "
                         "(include the experiment config to keep the sample-split test exact)")
    for section in ("primaryMetrics", "secondaryMetrics", "monitoringMetrics", "primary_metrics", "secondary_metrics"):
        if isinstance(data.get(section), list):
            data[section] = [_scale_pulse_metric(m, ctx, shares) for m in data[section]]
    for x in ("test", "control"):
        if doc.get(x):
            doc[x] = ctx.key.token("group", doc[x])
        if data.get(x):
            data[x] = ctx.key.token("group", data[x])
    doc.pop("message", None)
    return doc


def sanitize_request(doc, ctx):
    doc = copy.deepcopy(doc)
    ctx.control = ctx.control or doc.get("control")
    ctx.test = doc.get("test")
    for f in ("control", "test"):
        if doc.get(f):
            doc[f] = ctx.key.token("group", doc[f])
    if doc.get("experiment_id"):
        doc["experiment_id"] = ctx.key.token("experiment", doc["experiment_id"])
    return doc


def learn_config(doc, ctx):
    """Read group sizes and the control group before anything is scaled."""
    exp = doc.get("data", doc)
    for g in exp.get("groups", []) or []:
        if g.get("disabled"):
            continue
        for field in ("id", "name"):
            if g.get(field) is not None and g.get("size") is not None:
                ctx.sizes[str(g[field])] = float(g["size"])
    ctx.control = exp.get("controlGroupID") or exp.get("controlGroupId") or ctx.control


def sanitize_config(doc, ctx):
    key = ctx.key
    doc = copy.deepcopy(doc)
    exp = doc.get("data", doc)
    for field in ("id", "name"):
        if exp.get(field):
            exp[field] = key.token("experiment", exp[field])
    for field in ("layerID", "layerId", "targetingGateID", "targetingGateId", "assignmentSourceName",
                  "assignmentSourceExperimentName"):
        if exp.get(field):
            exp[field] = key.token("id", exp[field])
    for field in ("controlGroupID", "controlGroupId"):
        if exp.get(field):
            exp[field] = key.token("group", exp[field])
    for field in ("holdoutIDs", "holdoutIds"):
        if exp.get(field):
            exp[field] = [key.token("id", h) for h in exp[field]]
    if exp.get("inlineTargetingRulesJSON"):
        exp["inlineTargetingRulesJSON"] = "<targeting rules removed>"
    active = [g for g in exp.get("groups", []) or [] if not g.get("disabled")]
    for g in exp.get("groups", []) or []:
        for field in ("id", "name"):
            if g.get(field):
                g[field] = key.token("group", g[field])
        values = g.get("parameterValues") or {}
        g["parameterValues"] = {key.token("param", p): _param_value(v, key) for p, v in values.items()}
    for section in ("primaryMetrics", "secondaryMetrics"):
        for m in exp.get(section, []) or []:
            m["name"] = key.metric(m.get("name"), m.get("direction"))
            if isinstance(m.get("hypothesizedValue"), (int, float)):
                m["hypothesizedValue"] *= ctx.k
    for h in exp.get("healthChecks", []) or []:
        h.pop("metadata", None)
    for field in ("startTime", "endTime", "decisionTime", "createdTime", "lastModifiedTime"):
        if isinstance(exp.get(field), (int, float)):
            exp[field] = shift_epoch(exp[field], key.date_shift)
    if isinstance(exp.get("targetExposures"), (int, float)):
        exp["targetExposures"] = int(round(exp["targetExposures"] * ctx.u))
    exposures = exp.get("exposures")
    if isinstance(exposures, dict) and exposures:
        # exposures are keyed by group name or id; match each to its planned size
        real = list(exposures)
        shares = [ctx.sizes.get(str(g)) for g in real]
        counts = [exposures[g] for g in real]
        if all(isinstance(c, (int, float)) for c in counts):
            new = scale_counts(counts, shares if all(shares) and len(real) == len(active) else None, ctx.u)
            exp["exposures"] = {key.token("group", g): n for g, n in zip(real, new)}
    doc.pop("message", None)
    return doc


def _param_value(value, key):
    if isinstance(value, (dict, list)):
        return "<structured value>" if value else value
    return key.token("value", value)


def sanitize_audit(doc, ctx):
    key = ctx.key
    entries = doc.get("data", doc) if isinstance(doc, dict) else doc
    out = []
    for e in entries:
        e = dict(e)
        if e.get("name"):
            e["name"] = key.token("experiment", e["name"])
        if isinstance(e.get("changes"), dict):
            e["changes"] = {key.token("param", p) if p not in ("allocation", "groups", "size") else p:
                            v if p == "allocation" else "<changed>" for p, v in e["changes"].items()}
        if isinstance(e.get("time"), (int, float)):
            e["time"] = shift_epoch(e["time"], key.date_shift)
        out.append(e)
    return {"data": out} if isinstance(doc, dict) else out


# ---------- canonical files ----------

def _scale_canonical_metric(m, ctx, shares):
    key, k = ctx.key, ctx.k
    m = dict(m)
    real = str(m.get("metric", "metric")).partition(" - ")[0]
    if "metric" in m:
        m["metric"] = key.metric(m["metric"], m.get("directionality") or m.get("direction"))
    control = m.get("control_mean")
    s = key.mean_factor(real, control if isinstance(control, (int, float)) else None)
    for f in ("rel_delta",):
        if isinstance(m.get(f), (int, float)):
            m[f] *= k
    for f in ("rel_ci", "seq_rel_ci"):
        if isinstance(m.get(f), list):
            m[f] = [b * k if isinstance(b, (int, float)) else b for b in m[f]]
    if isinstance(control, (int, float)):
        if isinstance(m.get("test_mean"), (int, float)):
            m["test_mean"] = s * (control + k * (m["test_mean"] - control))
        m["control_mean"] = control * s
    elif isinstance(m.get("test_mean"), (int, float)):
        m["test_mean"] *= s
    for f in ("abs_delta", "control_se", "test_se"):
        if isinstance(m.get(f), (int, float)):
            m[f] *= s * k
    for f in ("abs_ci", "seq_abs_ci"):
        if isinstance(m.get(f), list):
            m[f] = [b * s * k if isinstance(b, (int, float)) else b for b in m[f]]
    if isinstance(m.get("control_units"), (int, float)) and isinstance(m.get("test_units"), (int, float)):
        m["control_units"], m["test_units"] = scale_counts([m["control_units"], m["test_units"]], shares, ctx.u)
    for f in ("segment",):
        if m.get(f):
            m[f] = key.token("segment", m[f])
    for f in ("test_group",):
        if m.get(f):
            m[f] = key.token("group", m[f])
    return m


def sanitize_scorecard(doc, ctx):
    doc = copy.deepcopy(doc)
    key = ctx.key
    ctx.control = ctx.control or doc.get("control_group")
    for c in doc.get("comparisons", []):
        shares = ctx.pair_shares(c.get("test_group"))
        c["metrics"] = [_scale_canonical_metric(m, ctx, shares) for m in c.get("metrics", [])]
        c["test_group"] = key.token("group", c.get("test_group"))
    for f in ("experiment_id",):
        if doc.get(f):
            doc[f] = key.token("experiment", doc[f])
    if doc.get("control_group"):
        doc["control_group"] = key.token("group", doc["control_group"])
    return doc


def learn_canonical_config(doc, ctx):
    for g in doc.get("groups", []) or []:
        if not g.get("disabled") and g.get("size_pct") is not None:
            for field in ("id", "name"):
                if g.get(field) is not None:
                    ctx.sizes[str(g[field])] = float(g["size_pct"])
    ctx.control = doc.get("control_group") or ctx.control


def sanitize_canonical_config(doc, ctx):
    key = ctx.key
    doc = copy.deepcopy(doc)
    for f in ("experiment_id", "name"):
        if doc.get(f):
            doc[f] = key.token("experiment", doc[f])
    for f in ("layer_id", "targeting_gate"):
        if doc.get(f):
            doc[f] = key.token("id", doc[f])
    if doc.get("control_group"):
        doc["control_group"] = key.token("group", doc["control_group"])
    if doc.get("inline_targeting"):
        doc["inline_targeting"] = "<targeting rules removed>"
    doc["holdouts"] = [key.token("id", h) for h in doc.get("holdouts") or []]
    for g in doc.get("groups", []):
        for f in ("id", "name"):
            if g.get(f):
                g[f] = key.token("group", g[f])
        g["parameters"] = {key.token("param", p): _param_value(v, key) for p, v in (g.get("parameters") or {}).items()}
    for section in ("primary_metrics", "secondary_metrics"):
        for m in doc.get(section, []) or []:
            m["metric"] = key.metric(m.get("metric"), m.get("direction"))
            if isinstance(m.get("hypothesized"), (int, float)):
                m["hypothesized"] *= ctx.k
    for h in doc.get("health_checks", []) or []:
        h.pop("metadata", None)
    for e in doc.get("edits", []) or []:
        if isinstance(e.get("time"), (int, float)):
            e["time"] = shift_epoch(e["time"], key.date_shift)
        if isinstance(e.get("changes"), dict):
            e["changes"] = {key.token("param", p) if p not in ("allocation", "groups", "size") else p:
                            v if p == "allocation" else "<changed>" for p, v in e["changes"].items()}
    if isinstance(doc.get("target_exposures"), (int, float)):
        doc["target_exposures"] = int(round(doc["target_exposures"] * ctx.u))
    exposures = doc.get("exposures") or {}
    if exposures:
        real = list(exposures)
        counts = [exposures[g] for g in real]
        shares = [ctx.sizes.get(str(g)) for g in real]
        if all(isinstance(c, (int, float)) for c in counts):
            new = scale_counts(counts, shares if all(shares) else None, ctx.u)
            doc["exposures"] = {key.token("group", g): n for g, n in zip(real, new)}
    return doc


def _threshold(spec, ctx, field, unit_field):
    if isinstance(spec.get(field), (int, float)):
        if spec.get(unit_field, "relative") == "absolute":
            spec[field] *= ctx.key.mean_factor(spec.get("_real", "metric")) * ctx.k
        else:
            spec[field] *= ctx.k


def _metric_spec(spec, ctx):
    spec = dict(spec)
    spec["_real"] = spec.get("metric")
    spec["metric"] = ctx.key.metric(spec.get("metric"), spec.get("direction"))
    _threshold(spec, ctx, "bar", "bar_unit")
    _threshold(spec, ctx, "margin", "margin_unit")
    spec.pop("_real")
    return spec


def sanitize_prereg(doc, ctx):
    key = ctx.key
    doc = copy.deepcopy(doc)
    for f in ("experiment_id", "name"):
        if doc.get(f):
            doc[f] = key.token("experiment", doc[f])
    if doc.get("test_group"):
        doc["test_group"] = key.token("group", doc["test_group"])
    primaries = doc.get("primaries") or {}
    if isinstance(primaries.get("metrics"), list):
        primaries["metrics"] = [_metric_spec(s, ctx) for s in primaries["metrics"]]
    for section in ("guardrails", "invariants"):
        if isinstance(doc.get(section), list):
            doc[section] = [_metric_spec(s, ctx) for s in doc[section]]
    doc["intended_params"] = [key.token("param", p) for p in doc.get("intended_params") or []]
    if doc.get("feature_metrics"):
        doc["feature_metrics"] = [key.metric(m) for m in doc["feature_metrics"]]
    if doc.get("hypothesis_metric"):
        doc["hypothesis_metric"] = key.metric(doc["hypothesis_metric"])
    if doc.get("segments"):
        doc["segments"] = [key.token("segment", s) for s in doc["segments"]]
    if isinstance(doc.get("pre_period"), dict):
        doc["pre_period"] = {key.metric(m): _scale_rel(v, ctx) for m, v in doc["pre_period"].items()}
    planned = doc.get("planned") or {}
    if isinstance(planned.get("units_per_arm"), (int, float)):
        planned["units_per_arm"] = int(round(planned["units_per_arm"] * ctx.u))
    return doc


def _scale_rel(v, ctx):
    if not isinstance(v, dict):
        return v
    v = dict(v)
    if isinstance(v.get("rel_delta"), (int, float)):
        v["rel_delta"] *= ctx.k
    if isinstance(v.get("rel_ci"), list):
        v["rel_ci"] = [b * ctx.k for b in v["rel_ci"]]
    return v


def sanitize_standards(doc, ctx):
    doc = copy.deepcopy(doc)
    if isinstance(doc.get("guardrails"), list):
        doc["guardrails"] = [_metric_spec(s, ctx) for s in doc["guardrails"]]
    if isinstance(doc.get("directions"), dict):
        doc["directions"] = {ctx.key.metric(m, d): d for m, d in doc["directions"].items()}
    for f in ("default_margin", "default_bar"):
        if isinstance(doc.get(f), (int, float)):
            doc[f] *= ctx.k
    return doc


def sanitize_daily(doc, ctx):
    out = []
    for p in doc:
        p = _scale_rel(p, ctx)
        if isinstance(p.get("seq_rel_ci"), list):
            p["seq_rel_ci"] = [b * ctx.k for b in p["seq_rel_ci"]]
        out.append(p)
    return out


def sanitize_evidence(doc, ctx):
    doc = copy.deepcopy(doc)
    shares = ctx.pair_shares()
    doc["metrics"] = [_scale_canonical_metric(m, ctx, shares) for m in doc.get("metrics", []) or []]
    segments = {}
    for metric, spec in (doc.get("segments") or {}).items():
        spec = dict(spec)
        if spec.get("by"):
            spec["by"] = ctx.key.token("dimension", spec["by"])
        spec["parts"] = [_scale_canonical_metric(p, ctx, shares) for p in spec.get("parts", [])]
        segments[ctx.key.metric(metric)] = spec
    if segments or "segments" in doc:
        doc["segments"] = segments
    return doc


# ---------- CSV ----------

def sanitize_csv(text, ctx, column_map, rows):
    key = ctx.key
    reader = list(csv.reader(io.StringIO(text)))
    if not reader:
        return text
    header, body = reader[0], reader[1:rows + 1]
    metric_col = column_map.get("metric")
    group_col = column_map.get("test_group")
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow([scrub_string(h, key) for h in header])
    for row in body:
        new = []
        for name, cell in zip(header, row):
            stripped = cell.strip()
            if not stripped:
                new.append(cell)
            elif name == metric_col or (not metric_col and re.search(r"metric|kpi", name, re.I)):
                new.append(key.metric(stripped))
            elif name == group_col:
                new.append(key.token("group", stripped))
            elif re.fullmatch(r"[<>~+\-−(\[]*[$€£¥]?\d[\d,]*(?:\.\d+)?(?:e-?\d+)?%?[)\]]*", stripped):
                new.append(scrub_numbers(cell, key, strict=True))
            elif re.fullmatch(r"[\d\s.,%+\-−()\[\]<>]+", stripped):
                new.append(scrub_numbers(cell, key, strict=True))
            else:
                new.append(key.token("label", stripped))
        writer.writerow(new)
    return out.getvalue()


# ---------- driver ----------

def kind_of(path, doc):
    name = os.path.basename(path).lower()
    if isinstance(doc, list):
        if doc and isinstance(doc[0], dict) and "rel_delta" in doc[0] and "metric" not in doc[0]:
            return "daily"
        if not doc or (isinstance(doc[0], dict) and ("actionType" in doc[0] or "changeLog" in doc[0])):
            return "audit"
        return "json"
    if not isinstance(doc, dict):
        return "json"
    data = doc.get("data", doc)
    if isinstance(data, dict) and any(s in data for s in ("primaryMetrics", "secondaryMetrics", "monitoringMetrics",
                                                           "primary_metrics")) and "groups" not in data:
        return "pulse"
    if isinstance(data, dict) and "groups" in data and ("parameterValues" in json.dumps(data["groups"])[:20000]
                                                         or "idType" in data or "controlGroupID" in data):
        return "config"
    if "groups" in doc and ("edits" in doc or "settings" in doc or "allocation_pct" in doc):
        return "canonical_config"
    if "comparisons" in doc:
        return "scorecard"
    if "primaries" in doc or ("guardrails" in doc and ("test_group" in doc or "planned" in doc or "intended_params" in doc)):
        return "prereg"
    if "guardrails" in doc or "srm_alpha" in doc or "directions" in doc:
        return "standards"
    if "segments" in doc or "cuts" in doc or ("metrics" in doc and isinstance(doc["metrics"], list)):
        return "evidence"
    if isinstance(data, list) and (not data or (isinstance(data[0], dict) and "actionType" in data[0])):
        return "audit"
    if "control" in doc and "test" in doc and not set(doc) - {"control", "test", "cuped", "confidence", "sequential",
                                                               "experiment_id", "as_of", "ci_level", "mc_correction"} - {
            k for k in doc if k.startswith("apply")}:
        return "request"
    return "audit" if "audit" in name else "json"


ORDER = ["config", "canonical_config", "request", "audit", "standards", "prereg", "pulse", "scorecard", "daily",
         "evidence", "json", "csv", "text"]
HANDLERS = {"config": sanitize_config, "canonical_config": sanitize_canonical_config, "request": sanitize_request,
            "audit": sanitize_audit, "standards": sanitize_standards, "prereg": sanitize_prereg,
            "pulse": sanitize_pulse, "scorecard": sanitize_scorecard, "daily": sanitize_daily,
            "evidence": sanitize_evidence}


def load_denylist(path):
    path = path or os.environ.get("DS_DENYLIST") or (os.path.join(os.environ["DS_OVERLAY_DIR"], "denylist.txt")
                                                     if os.environ.get("DS_OVERLAY_DIR") else None)
    if not path or not os.path.exists(path):
        return None
    terms = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.split("#", 1)[0].strip()
            if line:
                terms.append(line.lower())
    return terms


def read_names(path):
    if not path:
        return []
    with open(path, encoding="utf-8") as handle:
        return [line.split("#", 1)[0].strip() for line in handle if line.split("#", 1)[0].strip()]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--overlay", default=os.environ.get("DS_OVERLAY_DIR"),
                        help="holds sanitize_key.json, denylist.txt, metric_families.json and scorecard_map.json")
    parser.add_argument("--key", help="default: <overlay>/sanitize_key.json")
    parser.add_argument("--denylist", help="default: $DS_DENYLIST, else <overlay>/denylist.txt")
    parser.add_argument("--names", help="file of extra names to tokenize, one per line (features, teams, products)")
    parser.add_argument("--map", help="scorecard_map.json for a CSV (default: <overlay>/scorecard_map.json)")
    parser.add_argument("--rows", type=int, default=20, help="CSV rows to keep (default 20)")
    parser.add_argument("--scale-lifts", action="store_true", help="also hide relative changes, bars and margins")
    parser.add_argument("--seed", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    key_path = args.key or (os.path.join(args.overlay, "sanitize_key.json") if args.overlay else None)
    if not key_path:
        print("sanitize: set DS_OVERLAY_DIR or pass --key; the key must stay outside the output", file=sys.stderr)
        return 2
    out_dir = os.path.abspath(args.out_dir)
    if os.path.abspath(key_path).startswith(out_dir + os.sep):
        print("sanitize: the key would land in the output folder; keep it in the overlay", file=sys.stderr)
        return 2
    denylist = load_denylist(args.denylist or (os.path.join(args.overlay, "denylist.txt") if args.overlay
                                               and not os.environ.get("DS_DENYLIST") else None))
    if denylist is None:
        print("sanitize: no denylist found (DS_DENYLIST, <overlay>/denylist.txt or --denylist); refusing to run",
              file=sys.stderr)
        return 2
    library = explain.load_library(args.overlay)
    key = Key(key_path, library, args.seed, args.scale_lifts)
    for name in read_names(args.names):
        key.token("name", name)
    ctx = Context(key)
    map_path = args.map or (os.path.join(args.overlay, "scorecard_map.json") if args.overlay else None)
    column_map = {}
    if map_path and os.path.exists(map_path):
        with open(map_path, encoding="utf-8") as handle:
            column_map = json.load(handle)

    items = []
    for path in args.files:
        if path.lower().endswith(".json"):
            with open(path, encoding="utf-8") as handle:
                doc = json.load(handle)
            items.append((kind_of(path, doc), path, doc))
        else:
            with open(path, encoding="utf-8", errors="replace") as handle:
                items.append(("csv" if path.lower().endswith(".csv") else "text", path, handle.read()))
    items.sort(key=lambda item: ORDER.index(item[0]))
    names = [os.path.basename(p) for _, p, _ in items]
    if len(set(names)) < len(names):
        print("sanitize: two inputs share a file name; put them in separate runs or rename them", file=sys.stderr)
        return 2
    for kind, _, doc in items:  # learn the planned split before scaling any counts
        if kind == "config":
            learn_config(doc, ctx)
        elif kind == "canonical_config":
            learn_canonical_config(doc, ctx)
        elif kind == "request":
            ctx.control, ctx.test = doc.get("control") or ctx.control, doc.get("test")

    structured, outputs, counts = [], {}, {}
    for kind, path, doc in items:
        counts[kind] = counts.get(kind, 0) + 1
        if kind in HANDLERS:
            structured.append((path, HANDLERS[kind](doc, ctx)))
        elif kind == "json":
            structured.append((path, walk(doc, key, args.scale_lifts, numbers=True)))
        elif kind == "csv":
            outputs[os.path.basename(path)] = sanitize_csv(doc, ctx, column_map, args.rows)
        else:
            structured.append((path, doc))
    # second pass: every name is now known, so scrub all strings and text with the full key
    for path, doc in structured:
        name = os.path.basename(path)
        if isinstance(doc, str):
            outputs[name] = scrub_text(doc, key, args.scale_lifts)
        else:
            outputs[name] = json.dumps(walk(doc, key, args.scale_lifts), indent=1, ensure_ascii=False)
    families = key.families_out()
    if families:
        outputs["metric_families.json"] = json.dumps(families, indent=1)

    hits = {}
    for name, text in outputs.items():
        found = sorted({t for t in denylist if t in text.lower()})
        if found:
            hits[name] = found
    if hits:
        print("sanitize: denylist terms survive; nothing written. Add them to --names, or edit the source:",
              file=sys.stderr)
        for name, terms in hits.items():
            print(f"  {name}: {', '.join(terms)}", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    for name, text in outputs.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as handle:
            handle.write(text)
    key.save()
    kinds = ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
    print(f"sanitize: wrote {len(outputs)} files to {args.out_dir} ({kinds}); {len(key.strings)} names in the key")
    for note in dict.fromkeys(ctx.notes):
        print(f"sanitize: note: {note}")
    print("sanitize: free text (hypotheses, change logs, notes, readouts) is kept after scrubbing; "
          "read every file before sending it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
