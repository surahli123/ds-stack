Decision: Escalate

I wrote the readout to `readout.md`. The Test arm changed two things, so the review needs to decide whether to ship the bundle or re-test the ranker alone.

- **Primary (Successful Search Rate):**
  - It rose from 0.4120 to 0.4153, a relative lift of +0.81% (95% CI +0.41% to +1.21%, p=7e-5).
  - I read the pre-registered bar of 0.005 as relative, because the guardrail margins are relative. On that reading the point estimate clears it.
  - If the bar was meant as an absolute +0.005, it is not met (the absolute change is +0.0033). The team should confirm which was intended.
- **Guardrails:** All four pass on the worst end of the 95% CI. Revenue per User is close to its margin (worst end -0.8% against -1%).
- **Confound:** `snippet_length` went from 160 to 220 in Test, alongside the ranker change. The pre-registration lists only `ranker_model` as intended, and the audit log is empty, so there is no record of who added the snippet change or why. The lift can't be attributed to the ranker.
- **Secondary metrics:** CTR, Long Click Rate and Clicks per User are flat, so they don't corroborate the lift.
- **Segment results:** Some segments have p<0.05, but they come from many unplanned cuts without multiplicity correction. I treated them as exploratory only. Desktop success rate is negative (-0.66%, p=0.11), which is worth a follow-up.

The experiment ran the planned 14 days with balanced exposure and 1.0M users per arm, so I found no validity problems beyond the confound.

The review should decide three things:
1. Whether `snippet_length=220` is meant to ship. If the bundle is the intended launch, the evidence supports it.
2. Whether to re-run with `snippet_length` held at 160 in both arms. That is needed to claim the new ranker works.
3. Whether the 0.005 bar is relative or absolute.