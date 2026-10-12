Decision: Keep running

I saved the full readout to `readout.md`. The main points:

- **Primary metric:** Successful Search Rate is up 0.81% relative (41.20% → 41.53%, 95% CI ±0.40%, p = 7e-5). Read as a relative bar, that clears the pre-registered 0.5%. The pre-registration doesn't say whether 0.005 is relative or absolute. If it means an absolute +0.5 pp, the result fails (+0.33 pp). Someone should confirm which.
- **Effect is decaying:** The daily lift by days since exposure falls steadily from +1.5% on day 1 to +0.4% on day 12. From day 10 on, the daily CI includes 0, and day 12 is below the bar. The pooled +0.81% is an average over the inflated early days, so the steady-state lift may be under the bar or near zero. The series stops at day 12, although the plan was 14 days.
- **Guardrails:** Latency, abandonment, zero-result rate and revenue all sit inside their margins. The intervals are wide enough that small harms aren't ruled out.
- **Health:** Exposures are balanced, and the audit log is empty, so there were no mid-test changes. Only `ranker_model` differs between arms.
- **Segments and secondary metrics:** The few nominally significant results (CTR Head, CTR Tail, Clicks per User Tail) come from about 70 uncorrected comparisons, so I'd treat them as noise. Overall CTR and Long Click Rate are flat.

Next steps:
1. Re-pull Pulse. The current data is from 2026-09-25, and the test started 2026-09-12.
2. Ship if the latest daily effect is at least about 0.5% relative, its CI excludes harm, and the curve has flattened.
3. Don't ship if the curve keeps falling toward zero.