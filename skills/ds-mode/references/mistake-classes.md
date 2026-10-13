# Candidate mistake classes

These are candidates, not incidents. A class counts as an incident only once it happens in the analyst's own work. Archive rule: two real incidents before a new check is written.

Use this list to seed the wrong-number archive. When a wrong number turns up, find its class here (or add one), log the incident, and update the last column once a check exists.

## Classes

| Class | Mechanism | Detection rule | Covered today by |
|---|---|---|---|
| Outcome-based treatment assignment | Treated units are picked using the metric the effect is then measured on, so the effect is built into the selection. | Read how treated units were identified. Flag it when the selection variable is the outcome, or a function of it. | none yet. The causal-words rule shows the design; nothing tests it. |
| Seasonality as treatment | A seasonal swing inside the before/after window is credited to an intervention. | Flag it when the window spans a seasonal transition and the same calendar window a year earlier moved the same way with no intervention. | Partly. Seasonality is a standing alternative in the readout; no script compares with the prior year. |
| Post-hoc window extension | The post window is stretched or moved until the result looks right. | Flag it when the window was not fixed before the first query, or several windows were queried and one was reported. | none yet. The query log shows the windows tried; no script reads it. |
| Headline number from nowhere | A number in the headline matches no query or check output. | Flag any readout number that matches no logged query or check. | Tags resolved by `tools/verify_readout.py`. |
| Multiple testing without correction | Many tests at alpha 0.05 with no correction, so some significant results are chance. | Flag more than about 20 tests at alpha 0.05 with no Bonferroni or false-discovery-rate correction. | none yet. |

## Cases the classes came from, and what settles each

- Outcome-based assignment: a t-test on each region's before/after change in the outcome labeled 134 of 211 regions as treated; the true count was 11. Select on an input-side signal instead, such as spend dropping to zero.
- Seasonality as treatment: a four-month recovery in daily active users was credited to a model update shipped at the start of the window; the prior year showed the same recovery with no update. Run a difference-in-differences against the same calendar window a year earlier.
- Post-hoc window extension: the post window was moved to the seasonal peak after the effect was described as slow to build. Fix 30, 60 and 90 day windows before querying, and report all of them.
- Headline number from nowhere: the headline said 25.5% year over year, the charts showed 23.5% and 20.1%, and the correct figure was 20.0%. Every number traces to one query with a pinned formula.
- Multiple testing: 211 region-level tests at alpha 0.05, about 10 false positives expected with no real effect. Apply Bonferroni or a false-discovery-rate correction and report the family-wise error rate.

## Left out

- Free-side metrics for paying-side revenue: business framing (whether a strategy's metrics connect to the party that pays), not an analysis mechanic.
- Spec non-compliance: interview take-home compliance (an output whose grain or format contradicts a phrase in the prompt). The analysis version, a wrong grain, is covered by pinning the metric before querying.
- The interview-question field of every class.
