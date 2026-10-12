Decision: Escalate

**Summary.** Ranker v7 meets the pre-registered ship rule. But the primary metric, Queries per User, probably rose because users are reformulating, which is a bad sign. The launch review should make the call, not apply the rule mechanically.

**Pre-registered rule: met**

| Item | Result | Bar |
|---|---|---|
| Queries per User (primary) | 11.80 → 12.08, +2.4%, 95% CI about +1.5% to +3.3%, p<0.001 | Point estimate at least +1% (met); the whole CI is also above +1% |
| Latency p95 (guardrail) | +0.2%, 95% CI about −0.3% to +0.7% | Must not worsen by more than 2% (met) |

- **Design:** 14 days (2026-09-12 to 09-25), 1.0M users per arm against 0.9M planned, a 50/50 split, and the exposure-balance health check passed.
- **Config history:** the audit log is empty, so nothing changed mid-flight.
- **Analysis settings:** I read the unadjusted (CUPED off) results at 95% confidence, as requested. The config has no sequential testing and no Bonferroni correction.

**Why I'm not recommending Ship**
- **The experiment's own hypothesis isn't supported.** The config says the new ranker "raises the share of searches that end in a successful click," and its primary metric is Successful Search Rate. That metric is −0.35% (95% CI about −0.75% to +0.05%, p=0.09). CTR (−0.03%) and Long Click Rate (+0.26%) are flat, and Clicks per User is flat (−0.15%, p=0.71).
- **The extra queries look like a cost to users, not a gain.**
  - **Reformulation Rate:** +5.1% (0.143 → 0.150, p<0.001). It is a "lower is better" metric, so this is a significant move in the wrong direction.
  - **Time to First Click:** +1.3% (6.40 s → 6.48 s, p=0.012), also worse.
  - **Sessions per User:** −0.5% (p=0.054).
  - **Ad Click Rate:** −2.0% (p=0.001). Revenue per User is flat (−0.1%, p=0.78), so there is no confirmed revenue loss yet.
  - Together, this pattern fits users searching again because the first results weren't good enough.
- **The pre-registered primary doesn't match the config's hypothesis.** Queries per User is a volume metric with no built-in sense of quality. The prereg also has no guardrail on reformulation or on successful search. I can't tell from the files why the primary differs from the config.

**Caveats**
- **The segment cuts don't add up to the overall numbers.** For example, Reformulation Rate is down in most segments (mobile −2.0%, head queries −2.3%, desktop −0.8%) while overall it is +5.1%. Successful Search Rate overall (−0.35%) is lower than both its mobile (+0.19%) and desktop (−0.31%) cuts. Because of this, I put little weight on the segment results until the metric definitions and the Pulse export are checked.
- **There are about 50 secondary metrics at 95% with no multiplicity correction.** A few marginal p-values (for example Time to First Click at p=0.012) could be noise. The reformulation and ad-click results are strong enough that I don't think they are.

**For the review to decide**
1. Is the pre-registered Queries per User bar the right ship criterion, given that the result seems driven by reformulation? Whoever owns the prereg should answer this.
2. Before any ship decision, check why Reformulation Rate moved against its segments, and look at query-level reformulation sequences. If the reformulations are failed first searches, I'd recommend Don't ship.
3. Check whether the Ad Click Rate drop shows up in revenue over a longer window.

Shipping on the prereg alone is defensible. But it would be shipping a ranker that doesn't improve search success and appears to make users work harder.