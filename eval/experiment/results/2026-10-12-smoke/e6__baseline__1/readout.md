Decision: Escalate

# Ranker v7 – launch review readout

**Bottom line.** The pre-registered ship criteria are met, but the launch should not be approved on that alone. The experiment's own hypothesis (more successful searches) is not supported, and the evidence on whether the extra queries are good or bad is contradictory. A product owner needs to decide whether Queries per User is a valid success metric for this change. Until then I would not ship.

## Setup (checks pass)
- A/B test, unit = userID, 50/50 split (lambdamart_v6 vs v7; snippet_length is identical in both arms, so the only change is the intended `ranker_model`). Exposure-balance health check PASSED; 1.0M units per arm (plan was 900k).
- Started 2026-09-12, 14 days planned, Pulse snapshot 2026-09-25, so the planned duration is complete. No sequential testing, so a single final look is valid.
- Audit log is empty: no config changes after launch.
- Pulse was pulled with CUPED off and 95% CI, matching the prereg's CI level.

## Pre-registered criteria
| Item | Pre-reg | Result | Verdict |
|---|---|---|---|
| Primary: Queries per User, ship if point estimate ≥ +1% | +1% bar | **+2.4%** (11.80 → 12.08), 95% CI ≈ +1.5% to +3.3%, p<0.001 | Met (the CI lower bound also clears the bar) |
| Guardrail: Latency p95, no worse than +2% | 2% margin | +0.2% (412.0 → 412.8 ms), CI ≈ -0.3% to +0.7%, p=0.43 | Passed |

## Why I'm not recommending a plain Ship
1. **The pre-registered primary differs from the experiment's configured primary and hypothesis.** The Statsig config names *Successful Search Rate* as the primary metric, and the hypothesis is "raises the share of searches that end in a successful click." The prereg uses Queries per User instead. Nothing in the audit log explains the difference. On the configured primary, the ranker shows no benefit: -0.35% (41.2% → 41.06%), CI ≈ -0.75% to +0.05%, p=0.086. That is not significant, but the data cannot rule out a harm of about 0.75%.
2. **The secondary metrics do not support "more queries = more engagement."** Compared with control:
   - Clicks per User is flat (-0.15%, p=0.71).
   - CTR is flat (-0.03%, p=0.92).
   - Sessions per User is -0.49% (p=0.054).
   - Revenue per User is flat (-0.1%, p=0.78).
   - Long Click Rate is flat (+0.26%, p=0.39).
   - Time to First Click is **worse**: +1.3% (6.40 → 6.48 s), p=0.012.
   - Ad Click Rate is **down** 1.98%, p=0.001.
   - Reformulation Rate is reported **up** 5.1% (14.3% → 15.0%), p<0.001. Lower is better for this metric, and it is the most direct way for queries per user to rise through worse results. This is the single most important thing to resolve (see next point).
3. **The reformulation data is internally inconsistent.** The overall Reformulation Rate is +5.1%, but both platform slices are negative (Mobile -2.0%, Desktop -0.8%), and Mobile and Desktop should together cover all traffic. An overall effect cannot lie outside both of its parts. So either the overall figure or the slices are mis-defined or mis-computed. I can't tell which from the files I have. If the overall number is right, v7 plausibly raises queries by making users search again. If the slices are right, that story weakens. Data engineering should reconcile this before the review relies on either reading.
4. **A single reading of the primary says nothing about the mechanism.** More queries per user is only a win if users are getting value from them. Here, no outcome metric (success, clicks, long clicks, revenue) moves up with it.

## Other notes
- The slice metrics (about 44 cuts by device, query head/tail, and intent) were not pre-registered, and no multiple-comparison correction is applied. The few that cross p<0.05 (Head Clicks per User -2.1%, Navigational Long Click Rate +1.7%, Mobile and Head Reformulation) are roughly what chance gives at that count. I treat them as exploratory only and don't base the decision on them.
- Neither the 56 secondary metrics nor the prereg's single primary carries a multiplicity concern for the headline result; Queries per User is a single pre-registered test.

## What I'm asking the review to decide
1. Is Queries per User the right success criterion for this ranker? If the team confirms it is, the prereg rule says Ship. If the intended goal is successful searches, the result is a null-to-slightly-negative on that metric, and the answer is closer to "Don't ship."
2. Fix the Reformulation Rate discrepancy (overall vs. slices) and re-pull. This is a quick check, not a new experiment.
3. If both come back as the harmful reading (more reformulation, no gain in success), don't ship v7 as is.

No additional run time is needed; the sample and duration are complete.
