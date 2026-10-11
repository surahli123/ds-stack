"""Split a rate change into within-segment (rate) and segment-mix effects.

Kitagawa decomposition with midpoint weights, so the two effects sum exactly to
the overall change:

    delta = sum_s (r_after - r_before) * (w_after + w_before) / 2       # rate effect
          + sum_s (w_after - w_before) * ((r_after + r_before) / 2 - r)  # mix effect

where r is the midpoint of the overall rates. Subtracting r leaves the total
unchanged (the weight changes sum to zero) and makes each segment's mix term
readable: a segment adds to the drop only if its share grew and its rate is
below average, or its share shrank and its rate is above average.

Returns "flag" (a finding the answer must report, not a data defect) when mix
accounts for at least `threshold` of the movement, measured as
|mix| / (|mix| + |rate|) so offsetting effects (Simpson's paradox) still show,
AND the mix effect is larger than noise: at least `min_effect_pp` and at least
`z` standard errors of the overall change. Standard errors are binomial and
assume independent units; clustered units (sessions within users) make them
too small, so treat the intervals as a lower bound on the uncertainty.
"""

import math

from _common import COULD_NOT_RUN, FLAG, PASS, Result, SpecError, require

NAME = "mix_shift"
DEFAULT_THRESHOLD = 0.3
DEFAULT_MIN_EFFECT_PP = 0.1
DEFAULT_Z = 2.0
Z95 = 1.96


def _counts(segment, side):
    part = segment.get(side)
    if not isinstance(part, dict):
        raise SpecError(f"segment '{segment.get('name')}' is missing '{side}'")
    n = require(part, "n", int)
    k = require(part, "k", int)
    if k > n:
        raise SpecError(f"segment '{segment.get('name')}' {side}: k > n")
    return n, k


def _var(rate, n):
    return rate * (1 - rate) / n


def decompose(segments):
    parsed = []
    for segment in segments:
        name = segment.get("name", f"segment_{len(parsed)}")
        nb, kb = _counts(segment, "before")
        na, ka = _counts(segment, "after")
        if nb == 0 or na == 0:
            raise SpecError(f"segment '{name}' has n = 0 on one side; drop it or merge it")
        parsed.append((name, nb, kb, na, ka))
    total_b = sum(p[1] for p in parsed)
    total_a = sum(p[3] for p in parsed)
    overall_b = sum(p[2] for p in parsed) / total_b
    overall_a = sum(p[4] for p in parsed) / total_a
    midpoint = (overall_a + overall_b) / 2

    rate_effect = mix_effect = rate_var = 0.0
    per_segment = []
    for name, nb, kb, na, ka in parsed:
        wb, wa = nb / total_b, na / total_a
        rb, ra = kb / nb, ka / na
        weight = (wa + wb) / 2
        rate_part = (ra - rb) * weight
        mix_part = (wa - wb) * ((ra + rb) / 2 - midpoint)
        rate_effect += rate_part
        mix_effect += mix_part
        rate_var += weight ** 2 * (_var(rb, nb) + _var(ra, na))
        per_segment.append({
            "name": name, "n_before": nb, "n_after": na,
            "weight_before": round(wb, 6), "weight_after": round(wa, 6),
            "rate_before": round(rb, 6), "rate_after": round(ra, 6),
            "rate_effect_pp": round(100 * rate_part, 4), "mix_effect_pp": round(100 * mix_part, 4),
        })
    delta_se = math.sqrt(_var(overall_b, total_b) + _var(overall_a, total_a))
    return {
        "overall_before": overall_b, "overall_after": overall_a, "delta": overall_a - overall_b,
        "delta_se": delta_se, "rate_effect": rate_effect, "rate_effect_se": math.sqrt(rate_var),
        "mix_effect": mix_effect, "segments": per_segment,
        "smallest_segment_n": min(min(p[1], p[3]) for p in parsed),
    }


def _ci_pp(value, se):
    return [round(100 * (value - Z95 * se), 3), round(100 * (value + Z95 * se), 3)]


def run(spec):
    try:
        segments = require(spec, "segments", list)
        if len(segments) < 2:
            raise SpecError("needs at least 2 segments to separate mix from rate")
        threshold = float(spec.get("threshold", DEFAULT_THRESHOLD))
        min_effect_pp = float(spec.get("min_effect_pp", DEFAULT_MIN_EFFECT_PP))
        z = float(spec.get("z", DEFAULT_Z))
        parts = decompose(segments)
    except (SpecError, TypeError, ValueError) as err:
        return Result(NAME, COULD_NOT_RUN, f"could not run: {err}")

    rate, mix, delta = parts["rate_effect"], parts["mix_effect"], parts["delta"]
    moved = abs(rate) + abs(mix)
    share = abs(mix) / moved if moved > 1e-12 else 0.0
    noise_floor = max(min_effect_pp / 100, z * parts["delta_se"])
    details = {
        "overall_before": round(parts["overall_before"], 6),
        "overall_after": round(parts["overall_after"], 6),
        "delta_pp": round(100 * delta, 4),
        "delta_ci95_pp": _ci_pp(delta, parts["delta_se"]),
        "rate_effect_pp": round(100 * rate, 4),
        "rate_effect_ci95_pp": _ci_pp(rate, parts["rate_effect_se"]),
        "mix_effect_pp": round(100 * mix, 4),
        "mix_share": round(share, 4),
        "noise_floor_pp": round(100 * noise_floor, 4),
        "threshold": threshold, "min_effect_pp": min_effect_pp, "z": z,
        "smallest_segment_n": parts["smallest_segment_n"],
        "se_assumes_independent_units": True,
        "segments": parts["segments"],
    }
    lo, hi = details["rate_effect_ci95_pp"]
    summary = (f"overall change {100 * delta:+.2f} pp = within-segment {100 * rate:+.2f} pp "
               f"(95% CI {lo:+.2f} to {hi:+.2f}) + mix {100 * mix:+.2f} pp (mix share {share:.0%})")
    if share >= threshold and abs(mix) >= noise_floor:
        return Result(NAME, FLAG, "mix-dominant: " + summary + "; report the mix shift as part of the answer", details)
    if share >= threshold:
        summary += f"; the mix effect is within noise (floor {100 * noise_floor:.2f} pp)"
    return Result(NAME, PASS, summary, details)
