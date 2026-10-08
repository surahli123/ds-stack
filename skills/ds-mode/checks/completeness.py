"""Is the period you are about to report fully loaded?

Compares the target period's row count with the median of the periods before
it. Fails when the target is missing, below `min_ratio` of that median (late or
partial data), or above `max_ratio` when given (double loads).
"""

import statistics

from _common import COULD_NOT_RUN, FAIL, PASS, Result, SpecError, require

NAME = "completeness"
DEFAULT_MIN_RATIO = 0.8
DEFAULT_BASELINE_PERIODS = 7
MIN_BASELINE = 3


def run(spec):
    try:
        series = require(spec, "series", list)
        target = require(spec, "target", str)
        min_ratio = float(spec.get("min_ratio", DEFAULT_MIN_RATIO))
        max_ratio = spec.get("max_ratio")
        max_ratio = None if max_ratio is None else float(max_ratio)
        k = int(spec.get("baseline_periods", DEFAULT_BASELINE_PERIODS))
        rows = {}
        for point in series:
            period = require(point, "period", str)
            if period in rows:
                raise SpecError(f"period '{period}' appears twice")
            rows[period] = require(point, "rows", int)
    except (SpecError, TypeError, ValueError) as err:
        return Result(NAME, COULD_NOT_RUN, f"could not run: {err}")

    earlier = sorted(p for p in rows if p < target)[-k:]
    if len(earlier) < MIN_BASELINE:
        return Result(NAME, COULD_NOT_RUN,
                      f"could not run: need at least {MIN_BASELINE} periods before {target}, got {len(earlier)}")
    baseline = statistics.median(rows[p] for p in earlier)
    details = {"target": target, "baseline_periods": earlier, "baseline_median_rows": baseline,
               "min_ratio": min_ratio, "max_ratio": max_ratio}
    if target not in rows:
        return Result(NAME, FAIL, f"{target} has no rows loaded", details)
    if baseline == 0:
        return Result(NAME, COULD_NOT_RUN, "could not run: baseline median is 0 rows", details)

    ratio = rows[target] / baseline
    details.update(target_rows=rows[target], ratio=round(ratio, 4))
    summary = f"{target}: {rows[target]} rows = {ratio:.0%} of the trailing median ({baseline:g})"
    if ratio < min_ratio:
        return Result(NAME, FAIL, "incomplete: " + summary, details)
    if max_ratio is not None and ratio > max_ratio:
        return Result(NAME, FAIL, "possible double load: " + summary, details)
    return Result(NAME, PASS, summary, details)
