Decision: No effect found

I wrote the readout to `readout.md` in the working directory.

- **Primary metric:** Successful Search Rate moved from 41.20% to 41.22%, a change of +0.025pp (95% CI −0.099pp to +0.148pp, p=0.70). The pre-registered bar was +0.5pp, so the data rule out an effect that large. Don't ship v7 on this evidence.
- **Keep running:** I don't recommend extending the test. The planned 14 days have run, and the interval is already narrow. More days would not change the conclusion against a 0.5pp bar.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all sit well inside their margins. I read the margins as relative because `prereg.json` doesn't say. Abandonment passes either way.
- **Validity:**
  - The test ran as planned: 14 days from 2026-09-12 to 09-25, with 1.0M users per arm against a plan of 0.9M.
  - The balanced-exposure health check passed.
  - The audit log is empty, so there were no mid-test changes.
  - Only `ranker_model` differs between arms.
- **Tail queries:** Successful Search Rate on tail queries is +1.46pp (p<0.001). I flagged this as a lead for a separately pre-registered follow-up, not a result. It is one of about 56 unplanned slices, and it contrasts with the flat overall result and flat head, navigational and informational slices.