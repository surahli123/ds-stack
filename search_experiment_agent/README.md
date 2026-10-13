# Search experiment agent

An agent that turns one search A/B experiment into a readout the triage meeting can act on.

Input: a name, a config ID or a console URL.

What it does:
1. Checks the setup and the data (M0).
2. Explains why each metric moved (M1), running the deep-dive cuts it can script against the query-level table.
3. Says whether the flight is ready for triage.
4. Cites what confirmed, similar past experiments taught.

Every run leaves a trace. Reviewed traces become typed lessons. A lesson changes the agent's knowledge only after a paired evaluation passes on held-out flights and a person approves it.

This prototype runs at home on a synthetic warehouse shaped like the work one. The analysis core is ds-stack's `ds-experiment` tools, used unchanged.

## How a run goes

1. Resolve the input to the config (if available) and the experiment name that keys T1, the vendor scorecard table.
2. Read T1's latest snapshot and its daily series.
3. **M0** checks config, sample split, metric coverage, consistency, power, data quality and duration. Each is PASS, WARN, BLOCK or UNKNOWN, with its source. `docs/specs/stage-contract.md` turns these into a grade per arm: `not_permitted`, `directional_only` or `decision_grade`.
4. **M1** works one arm at a time:
   - decide.py makes the launch call, and explain.py matches the enterprise patterns.
   - The agent runs each scripted cut through a fixed, read-only runner, joined to the assignment source and the paying cohort. Each cut is a ratio of sums per user, so its numbers tie to T1.
   - Each result confirms or refutes a pattern by script, and the grade is recomputed after every action.
5. Render the readout and a triage prep per arm, then write the trace, a review form, a card draft and the frozen case.

## Results at home

All results below are on synthetic flights.

- **Grade and mechanism, 9 flights.** The planted grade comes out on 9 of 9. The planted mechanism comes out on 7 of 9.
  - The two misses share a renamed placement metric. A one-line mapping lesson learned on the first fixes the second, which it never saw.
- **Evidence behind findings.** Every confirmed finding names the statement that confirmed it, and no run has an unsupported claim.
- **The learning loop:**
  - A mapping lesson passes with 0 regressions on 8 held-out cases and improves the 1 it should.
  - A harmful lesson fails on the case it would break.
  - After approval, a confirmed card is cited in the next similar flight's readout.

## Layout

- `search_agent/`: the run (`run.py`)
  - `sources/`: warehouse, T1, config, resolver
  - `m0/`: checks and the grade
  - `m1/`: method, cut runner, enterprise pattern library, cut templates
  - `render/`: the readout
  - `trace.py`
- `learning/`: cards, lessons, paired evaluation and approval, the knowledge version, the `loop` command
- `.agents/skills/`: `search_m0_readiness`, `search_m1`
- `docs/specs/`: the stage contract
- `overlay.example/`: warehouse settings, standards, contracts
- `synth/`: the synthetic warehouse
- `tests/`: unittest only

## Try it

```
python3 synth/make_warehouse.py --out /tmp/synth
cp /tmp/synth/contracts/*.json overlay.example/contracts/
python3 -m search_agent.run --experiment synth-3p-boost-mid --overlay overlay.example \
    --warehouse sqlite:/tmp/synth/warehouse.sqlite --configs /tmp/synth/configs --out /tmp/runs/mid
python3 -m unittest discover -s tests
```

`learning/loop.py` documents the loop, one command per step: freeze, propose, evaluate, approve, stamp, confirm-card, stats.
