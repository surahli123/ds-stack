I wrote the readout to `readout.md`. Its first line is `Decision: Can't tell`.

The Pulse I was given is a snapshot from 2026-09-15, only 3 days into a 14-day experiment. It has about 261k users per arm against the 900k planned, and today is 2026-10-12. The experiment also has no sequential testing, so a mid-run p-value isn't valid for a ship call.

- **Primary metric:** Successful Search Rate is up +0.00585 (p=0.011), above the +0.005 bar. The 95% CI runs from about +0.0013 to +0.0104, so the true lift could be well below the bar.
- **Bar interpretation:** I read the +0.005 bar as an absolute change. The pre-registration doesn't say, so that's an assumption.
- **Guardrails:** Latency, abandonment, zero-result rate and revenue per user all stay inside their pre-registered margins. I read the margins as relative, matching Pulse's percent change.
- **Segment metrics:** About 60 segment metrics showed nothing worth acting on. Two sit near p=0.05, which is expected from that many uncorrected looks.
- **Config:** The config looks clean. The arms are 50/50, the exposure-balance check passed, and only `ranker_model` differs between arms. The audit log is empty, so there were no mid-flight changes. The experiment is still marked active well past its planned end, which someone should explain.

The readout recommends re-pulling Pulse with the same settings and deciding against the pre-registered bar.