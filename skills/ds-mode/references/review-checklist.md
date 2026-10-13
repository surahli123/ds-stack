# Review checklist

What a reviewer verifies in a ds-mode readout, in order. The reviewer is a person or a fresh-context subagent that sees the request, the readout and the logs, not the analyst's reasoning. Every item is a yes/no question. Cheap, mechanical items come first, so a review fits in under 10 minutes.

## 1. Do the numbers resolve?

Run `tools/verify_readout.py` on the readout and its logs before reading anything else.

- Does every number carry a tag, and does each tag resolve to a logged query `[q<n>]`, a logged check `[check:<name>#<n>]`, or the request `[given]`?
- Does each tagged query compute what its sentence says (filter, period, grain)?

If this fails, send it back now. Nothing below means anything for a number nobody can trace.

## 2. Is it the right metric?

- Does the Provenance definition (numerator, denominator, filters, grain, source table) match the source of truth, or is it labeled `[guess]`?
- Does the reconciliation line tie the base number to a known figure, with any gap explained?
- If the metric is a proxy for what the decision cares about, does the readout say so?

## 3. Is it the question that was asked?

- Does the restated question match the request, no narrower and no broader, and is the decision named?
- If the request had two readings, did the analyst ask, or state the reading used and put the other in the caveats?

## 4. Do the alternatives rule things in or out?

- Are the standing alternatives all there: mix-shift, seasonality and day of week, data completeness, logging or definition changes, and the requester's cause?
- Would each piece of evidence look different if its alternative were true? A check that can't see the alternative doesn't rule it out.
- Could something else that changed at the same time (a launch, a pricing change, a tracking change) explain the move, and is it addressed?
- Are the comparison windows the same length, the same weekdays and complete, and were they fixed before the results were seen?
- Are segments defined the same way on both sides, and did a coarser grain agree with the finer one?

## 5. Did the right checks run, and did their statuses land?

- Did every applicable check run: `completeness` for each period, `fanout` after each join, `mix_shift` for a moved rate, `srm` before an experiment lift? Is each skipped one explained?
- Does each check line match the logged output exactly?
- Does each `fail` change the answer, or does the readout show with evidence why not? If it can't be resolved, is the headline `can't tell`?
- Does each `flag` show up in the Answer as how much of the move is mix and how much is within-segment?

## 6. Does causal language match the design?

- Do "caused", "drove" and "because of" appear only for a randomized test or a design that identifies the cause?
- Otherwise, does the text say "coincided with" or "is associated with" and name what would confirm it?
- Were treated units chosen by something other than the outcome being measured?

## 7. Is the interval compared with the threshold?

- Is there a 95% interval, or `(no interval: <reason>)` with a reason that holds?
- Does the decision section compare the interval with the smallest change that would alter the decision?
- If the interval spans that threshold, does the readout say `can't tell` or name the uncertainty, not call it from the point estimate?
- Is the sample large enough for the effect size that matters?

## 8. Would a caveat change the answer?

- Is each listed caveat followed by what would settle it?
- Is any missing: a sample that doesn't represent the population the decision covers, an unverified definition, an incomplete period?

## When an item fails

Send the readout back with the item number and the question that failed. Don't fix it yourself or patch the number silently: the analyst owns the number, and a quiet fix hides how it went wrong. Review again from item 1 after the fix. If a wrong number had already reached a reader, log it in the wrong-number archive (see `mistake-classes.md`).
