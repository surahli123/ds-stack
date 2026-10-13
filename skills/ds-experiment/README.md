# ds-experiment

An experiment readout for search A/B tests that answers what the triage meeting asks: is the result trustworthy, what's the call, why did each metric move, and is it ready for triage. The launch call and the readiness verdict are computed by scripts. The model feeds the scripts, runs the deep-dive cuts and writes at most three labelled bullets per section.

## What it produces

| File | For | Contents |
|---|---|---|
| `readout.md` | the launch review | the call, the ask, status, what could reverse it, the deciding metric first, checks |
| `triage_prep.md` | the engineer presenting | standard questions, each metric question with candidates and evidence, cuts run and to run, what was ruled out |
| `decision.json`, `explain.json` | the record | every verdict, check, candidate and cut result |

## How it works

1. `normalize.py` turns a Statsig Pulse response (or a CSV export through `scorecard_map.json`) and the experiment config into canonical files. Request-side settings such as CUPED and the confidence level come from `request.json`, because the response doesn't carry them.
2. `decide.py` gives each registered metric a verdict from its interval against its own bar or margin, and makes the call as a fixed function of those verdicts and the validity checks. Only the primary and registered guardrails can block a launch.
3. `explain.py` reads the scorecard against a library of search metric patterns, each with a published source:
   - more clicks without more satisfaction
   - activity without success
   - speed cost
   - good and bad abandonment
   - a ratio moved by its denominator
   - segment concentration and segments that don't add up

   It lists the questions triage will ask and the cuts that would confirm or refute each candidate. When a cut's result comes back in `evidence.json`, a supported candidate is confirmed and a contradicted one is removed.
4. `render.py` writes the two documents. It refuses model text with stat-speak or numbers that aren't in the scorecard.

## Triage readiness

The verdict is one of three, and it names what to do first:

- **Not ready** when:
  - a validity check failed
  - the test needs more data
  - the effect fades by exposure day
  - the segments don't add up to the total
  - two opposite explanations could change the call
  - a Ship call's best explanation is bad news
- **Ready, with open questions** for:
  - a borderline deciding result
  - unknown durability
  - a primary too noisy to read
  - a movement with no candidate
  - exploratory findings on registered metrics
- **Ready** when every movement triage will ask about has a candidate and none conflict.

The thresholds follow published practice: Statsig's sample-split bands, Spotify's decision rule, Microsoft's review checklists and Bing's rerun experience with borderline wins. The research notes are in `research_notes/`, outside the repo.

## Results so far

All on synthetic search experiments, about 57 metrics each; real experiments come next, on the work laptop.

| Eval | ds-experiment | Plain prompting |
|---|---|---|
| Launch call, 27 cases x 3 runs | 81 of 81 runs right; passes the pre-registered rule | 48% of cases; ships a blocker in 6 runs |
| Fresh reader recovers the call and ask from a skim | 79% | 9% |
| Stat-speak terms per readout | 1.3 | 9.0 |

The deep-dive layer passes its 9 planted-mechanism cases and 45 adversarial regression cases in pytest. Those cases were built alongside the pattern library, so they show the pipeline works, not that it generalizes.

## On the work laptop

See `port/README.md`: write the overlay's `standards.json` and `metric_families.json`, self-test the adapter, measure the current agent's readouts with `port/audit_readouts.py`, and backtest `decide.py` against past triage calls with `port/backtest.py`. Both scripts print counts only.
