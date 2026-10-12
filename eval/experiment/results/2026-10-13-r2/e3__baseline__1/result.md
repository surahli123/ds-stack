Decision: Don't ship

I wrote the readout to `readout.md` in the work directory. Ranker v7 lifts Successful Search Rate by a small amount that falls well short of the pre-registered bar.

- **Primary metric:** Successful Search Rate rose from 0.4120 to 0.4133, a change of +0.0013. The 95% CI is [+0.0005, +0.0020], so the lift is real (p=0.0007). It is about a quarter of the +0.005 bar, and even the top of the CI stays below the bar. The result is the same whether the bar is read as an absolute or a relative change.
- **Guardrails:** All four pass on the worse end of their CIs. Revenue per User comes closest: its CI floor is about −0.8% against a −1% margin.
- **Validity:** The experiment ran the planned 14 days with 1M users per arm, balanced exposure, and no config changes (the audit log is empty). The only difference between arms is `ranker_model`.
- **Segments:** Nothing is meaningful. One navigational CTR result (p=0.023) is nominally significant, but it is one of about 60 unplanned cuts, so I treated it as noise.
- **Pulse date:** The pulse is dated 2026-09-25 and the experiment still shows "active" today. If it has kept running since, I haven't analysed the later data.
- **Your call:** If the team wants to ship a +0.1–0.2pp gain anyway, that means lowering the bar after seeing the data, and the readout says to argue it openly as a new decision.