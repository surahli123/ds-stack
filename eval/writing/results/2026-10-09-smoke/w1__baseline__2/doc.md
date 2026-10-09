# Ranker v2 and the CTR drop: readout for Dana

**Decision needed by Thursday:** roll back v2 or not.

## Recommendation

**Don't roll back v2.** The CTR drop is explained by a shift in traffic toward mobile, not by a change in how either platform performs. Two follow-ups are worth doing, but neither should block the decision (see "What would change this").

## What happened

Overall CTR fell from 30.4% in the week before v2 reached 100% (Sep 28) to 28.3% the week after, a drop of 2.1 pp.

Within each platform, CTR did not move:

| | Before | After |
|---|---|---|
| Desktop CTR | 36.0% | 36.0% |
| Mobile CTR | 22.0% | 22.0% |
| Mobile share of searches | 40% | 55% |

Mobile has a much lower CTR than desktop. When mobile grew from 40% to 55% of searches, the blended CTR fell even though neither platform got worse. A standard mix decomposition puts the split at:

- **Mix effect (traffic shift): -2.10 pp**
- **Within-platform effect (ranking quality): -0.0001 pp**

Essentially all of the drop is mix. The simple check agrees: 0.6 × 36.0 + 0.4 × 22.0 = 30.4, and 0.45 × 36.0 + 0.55 × 22.0 = 28.3.

## What I ruled out

- **Missing data:** all 14 days are present, with 4 rows per day (platform × country) and flat row counts.
- **Country:** US fell from 31.3% to 29.2% and other countries from 29.3% to 27.3%. Both fell about 2 pp, so the drop is not specific to one country. This fits the mix explanation, because the mobile shift cuts across countries.

## Open item: why did mobile traffic jump?

Growth said there may have been an app store feature that week, but this is **not confirmed**. The explanation above holds regardless of the cause, since the data shows the shift happened. But if the cause turns out to be something v2 did (for example, v2 making mobile search more attractive), the story changes. Growth needs to confirm.

## Limits of this analysis

- **Before/after only.** v2 went to everyone at once, so there was no holdout. A small v2 effect, under about 0.3 pp, would not be visible in this data.
- **CTR only.** I did not properly check long clicks or reformulation rate. A quick look at long clicks showed them flat, but that was not a rigorous check. A ranker could keep CTR flat and still hurt result quality.
- **Metric definition.** The numbers above come from the table, where CTR is clicks over all searches. The dashboard uses searches with results shown as the denominator, which gives numbers about 0.5 pp different. The drop is the same under both. If you quote figures, use the dashboard definition. I have not restated these figures on that basis.

## What would change this

1. **Growth can't explain the mobile jump, or ties it to v2.** Revisit the decision.
2. **Long clicks or reformulation rate got worse.** That would suggest a quality problem that CTR hides.
3. **You need certainty about v2 itself.** The only way to get it is a holdout: keep 5% of traffic on the old ranker for two weeks and compare directly.

## Next steps

| Action | Owner |
|---|---|
| Confirm whether an app store feature drove the mobile jump | Growth |
| Properly check long clicks and reformulation rate, split by platform | Analysis |
| Decide whether to run the 5% holdout for two weeks | Dana |
