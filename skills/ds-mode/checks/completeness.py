"""Is the period you are about to report fully loaded?

Compares the target period's row count with the median of earlier periods.
Daily ISO dates are compared with the same weekday (the last `baseline_periods`
same-weekday days, default 4), so a normal Saturday isn't read as a partial
load. With under three weeks of history it falls back to the trailing 7 days
and says so. Any other period labels use the trailing `baseline_periods`
(default 7).
Fails when the target is missing, below `min_ratio` of that median (default
0.9: late or partial data), or above `max_ratio` when given (double loads).
"""

import statistics
from datetime import date

from _common import COULD_NOT_RUN, FAIL, PASS, Result, SpecError, require

NAME = "completeness"
DEFAULT_MIN_RATIO = 0.9
MIN_BASELINE = 3


def _as_date(label):
    try:
        return date.fromisoformat(label)
    except ValueError:
        return None


def run(spec):
    try:
        series = require(spec, "series", list)
        target = require(spec, "target", str)
        min_ratio = float(spec.get("min_ratio", DEFAULT_MIN_RATIO))
        max_ratio = spec.get("max_ratio")
        max_ratio = None if max_ratio is None else float(max_ratio)
        rows = {}
        for point in series:
            period = require(point, "period", str)
            if period in rows:
                raise SpecError(f"period '{period}' appears twice")
            rows[period] = require(point, "rows", int)
    except (SpecError, TypeError, ValueError) as err:
        return Result(NAME, COULD_NOT_RUN, f"could not run: {err}")

    dates = {p: _as_date(p) for p in list(rows) + [target]}
    daily = all(dates.values())
    if daily:
        prior = sorted((p for p in rows if dates[p] < dates[target]), key=dates.get)
        earlier, basis = [], "trailing days"
        if spec.get("same_weekday", True):
            earlier = [p for p in prior if dates[p].weekday() == dates[target].weekday()][-int(spec.get("baseline_periods", 4)):]
            basis = "same weekday"
        if len(earlier) < MIN_BASELINE:
            earlier = prior[-int(spec.get("trailing_days", 7)):]
            basis = "trailing days" if basis == "trailing days" else "trailing days (under 3 weeks of same-weekday history)"
    else:
        k = int(spec.get("baseline_periods", 7))
        earlier = sorted(p for p in rows if p < target)[-k:]
        basis = "trailing periods"
    if len(earlier) < MIN_BASELINE:
        return Result(NAME, COULD_NOT_RUN,
                      f"could not run: need at least {MIN_BASELINE} earlier periods ({basis}) before {target}, got {len(earlier)}")
    baseline = statistics.median(rows[p] for p in earlier)
    details = {"target": target, "basis": basis, "baseline_periods": earlier, "baseline_median_rows": baseline,
               "min_ratio": min_ratio, "max_ratio": max_ratio}
    if target not in rows:
        return Result(NAME, FAIL, f"{target} has no rows loaded", details)
    if baseline == 0:
        return Result(NAME, COULD_NOT_RUN, "could not run: baseline median is 0 rows", details)

    ratio = rows[target] / baseline
    details.update(target_rows=rows[target], ratio=round(ratio, 4))
    summary = f"{target}: {rows[target]} rows = {ratio:.0%} of the {basis} median ({baseline:g})"
    if ratio < min_ratio:
        return Result(NAME, FAIL, "incomplete: " + summary, details)
    if max_ratio is not None and ratio > max_ratio:
        return Result(NAME, FAIL, "possible double load: " + summary, details)
    return Result(NAME, PASS, summary, details)
