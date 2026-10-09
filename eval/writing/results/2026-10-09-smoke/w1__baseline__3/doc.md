# Ranker v2 and the CTR drop: readout for Dana

**Decision needed by Thursday:** roll back ranker v2?

**Recommendation: don't roll back.** The CTR drop is explained almost entirely by a shift in traffic toward mobile, not by a change in how v2 ranks results. One caveat limits how firmly we can say v2 had no effect (see "What this can't tell us").

## What happened

v2 went to 100% of traffic on Sep 28. Comparing the week before and the week after, overall search CTR fell from **30.4% to 28.3% (-2.1 pp)**.

## What we found

| | Week 1 | Week 2 |
|---|---|---|
| Overall CTR | 30.4% | 28.3% |
| Desktop CTR | 36.0% | 36.0% |
| Mobile CTR | 22.0% | 22.0% |
| Mobile share of searches | 40% | 55% |

- **Within each platform, CTR didn't move.** Desktop and mobile are each flat. If v2 had made results worse, we'd expect at least one of them to drop.
- **Mobile has a lower CTR than desktop, and mobile's share of searches rose from 40% to 55%.** That pulls the blended number down.
- **A mix decomposition attributes essentially all of the drop to the mix shift:** -2.10 pp from mix, about -0.0001 pp from within-platform change.
- **Country isn't the explanation.** US went 31.3% to 29.2% and other countries 29.3% to 27.3%. Both fell about 2 pp, so the drop isn't specific to a region.
- **The data is complete:** all 14 days present, 4 rows per day (platform x country), row counts flat.

## What we don't know yet

- **Why mobile traffic jumped.** Growth thinks there may have been an app store feature that week. This is unconfirmed.

## What this can't tell us

- **There was no holdout.** v2 went to everyone at once, so this is a before/after comparison only. A small v2 effect (under roughly 0.3 pp) would be invisible here.
- **I only looked at CTR.** A quick check suggested long clicks were flat, but I didn't do it properly. I haven't looked at reformulation rate.

## Next steps

1. **Growth:** confirm what drove the mobile traffic increase (app store feature or something else). This closes the one open question in the explanation.
2. **Optional, if you want certainty about v2 itself:** run a 5% holdout for two weeks. That is the only way to detect a small effect.
3. **Optional, low cost:** do the long-click and reformulation-rate checks properly.

## Note on metric definitions

The dashboard computes CTR over searches with results shown. The underlying table uses all searches. The two differ by about 0.5 pp in level, but the size of the drop is the same in both. Use the dashboard definition when quoting numbers. Check that the figures above are on that basis before sharing them externally.
