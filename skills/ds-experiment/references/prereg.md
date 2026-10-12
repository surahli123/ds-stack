# prereg.json: the pre-registration decide.py reads

Write it from the team's pre-registration (the experiment's hypothesis field, the launch doc). Copy what the team wrote. Never invent a bar or a margin: leave a field out and the team standard in the overlay fills it, and the readout says so. Set `"confirmed": false` until the owner has checked it.

```json
{
  "experiment_id": "ranker_v7", "name": "Ranker v7", "design": "ab", "unit": "userID",
  "test_group": "Test", "confirmed": false, "source": "hypothesis field and launch doc, 2026-09-10",
  "ci_level": 0.95, "planned": {"days": 14, "units_per_arm": 900000}, "sequential": false,
  "primaries": {"rule": "all", "ship_requires": "point_at_bar", "metrics": [
    {"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005}]},
  "guardrails": [
    {"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.02},
    {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.01}],
  "invariants": [{"metric": "Exposures per User"}],
  "intended_params": ["ranker_model"],
  "explanations": [],
  "pre_period": {}
}
```

| Field | Meaning |
|---|---|
| `metric` | the scorecard's metric name, exactly. A near miss binds nothing and the metric reads as missing |
| `direction` | the good direction: `increase` or `decrease`. A metric with none can only escalate |
| `bar` | the smallest primary change worth launching, as a fraction (0.005 = 0.5%); `bar_unit: "absolute"` for absolute |
| `ship_requires` | `point_at_bar` (default: the estimate clears the bar), `ci_at_bar` (the whole interval does) or `ci_excludes_zero` |
| `rule` | `all` primaries must improve, or `any` (then the primaries share the error rate) |
| `margin` | the largest guardrail harm tolerated, as a fraction; leave it out for a regression check against zero |
| `mass_share` | for a primary measured on triggered traffic: the triggered share of the control metric's total, to convert the lift to overall |
| `intended_params` | the config parameters the test is meant to change; any other difference between arms fails the config check |
| `explanations` | `{check, cause, evidence}` for a known sample-split or pre-period problem. Only these can soften a failed check, and they escalate rather than ship |
| `pre_period` | `{metric: {rel_delta, rel_ci}}` from a pre-exposure comparison, when the platform doesn't run one |
| `design` | `ab`, `interleaving` or `holdout`. Only `ab` gets a launch call |

Directions are not obvious for search metrics. Queries per user, reformulation, abandonment and time to first click can move either way for good or bad reasons. Use the team's direction, and say in the notes when the mechanism contradicts it.
