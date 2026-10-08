"""Split a rate change into within-segment (rate) and segment-mix effects.

Kitagawa decomposition with midpoint weights, so the two effects sum exactly to
the overall change:

    delta = sum_s (r_after - r_before) * (w_after + w_before) / 2   # rate effect
          + sum_s (w_after - w_before) * (r_after + r_before) / 2   # mix effect

Fails when mix accounts for at least `threshold` of the movement, measured as
|mix| / (|mix| + |rate|) so offsetting effects (Simpson's paradox) still show,
and the mix effect is at least `min_effect_pp` percentage points (default 0.1),
so a flat metric's noise is not flagged.
"""

from _common import COULD_NOT_RUN, FAIL, PASS, Result, SpecError, require

NAME = "mix_shift"
DEFAULT_THRESHOLD = 0.3
DEFAULT_MIN_EFFECT_PP = 0.1


def _counts(segment, side):
    part = segment.get(side)
    if not isinstance(part, dict):
        raise SpecError(f"segment '{segment.get('name')}' is missing '{side}'")
    n = require(part, "n", int)
    k = require(part, "k", int)
    if k > n:
        raise SpecError(f"segment '{segment.get('name')}' {side}: k > n")
    return n, k


def decompose(segments):
    totals = {"before": 0, "after": 0}
    parsed = []
    for segment in segments:
        name = segment.get("name", f"segment_{len(parsed)}")
        nb, kb = _counts(segment, "before")
        na, ka = _counts(segment, "after")
        if nb == 0 or na == 0:
            raise SpecError(f"segment '{name}' has n = 0 on one side; drop it or merge it")
        parsed.append((name, nb, kb, na, ka))
        totals["before"] += nb
        totals["after"] += na

    rate_effect = mix_effect = 0.0
    per_segment = []
    k_before = k_after = 0
    for name, nb, kb, na, ka in parsed:
        wb, wa = nb / totals["before"], na / totals["after"]
        rb, ra = kb / nb, ka / na
        rate_part = (ra - rb) * (wa + wb) / 2
        mix_part = (wa - wb) * (ra + rb) / 2
        rate_effect += rate_part
        mix_effect += mix_part
        k_before += kb
        k_after += ka
        per_segment.append({
            "name": name,
            "weight_before": round(wb, 6), "weight_after": round(wa, 6),
            "rate_before": round(rb, 6), "rate_after": round(ra, 6),
            "rate_effect_pp": round(100 * rate_part, 4), "mix_effect_pp": round(100 * mix_part, 4),
        })

    overall_before = k_before / totals["before"]
    overall_after = k_after / totals["after"]
    return {
        "overall_before": overall_before,
        "overall_after": overall_after,
        "delta": overall_after - overall_before,
        "rate_effect": rate_effect,
        "mix_effect": mix_effect,
        "segments": per_segment,
    }


def run(spec):
    try:
        segments = require(spec, "segments", list)
        if len(segments) < 2:
            raise SpecError("needs at least 2 segments to separate mix from rate")
        threshold = float(spec.get("threshold", DEFAULT_THRESHOLD))
        min_effect_pp = float(spec.get("min_effect_pp", DEFAULT_MIN_EFFECT_PP))
        parts = decompose(segments)
    except (SpecError, TypeError, ValueError) as err:
        return Result(NAME, COULD_NOT_RUN, f"could not run: {err}")

    rate, mix = parts["rate_effect"], parts["mix_effect"]
    moved = abs(rate) + abs(mix)
    share = abs(mix) / moved if moved > 1e-12 else 0.0
    details = {
        "overall_before": round(parts["overall_before"], 6),
        "overall_after": round(parts["overall_after"], 6),
        "delta_pp": round(100 * parts["delta"], 4),
        "rate_effect_pp": round(100 * rate, 4),
        "mix_effect_pp": round(100 * mix, 4),
        "mix_share": round(share, 4),
        "threshold": threshold,
        "min_effect_pp": min_effect_pp,
        "segments": parts["segments"],
    }
    summary = (
        f"overall change {100 * parts['delta']:+.2f} pp = within-segment {100 * rate:+.2f} pp "
        f"+ mix {100 * mix:+.2f} pp (mix share {share:.0%})"
    )
    if share >= threshold and abs(100 * mix) >= min_effect_pp:
        return Result(NAME, FAIL, "mix-shift: " + summary, details)
    return Result(NAME, PASS, summary, details)
