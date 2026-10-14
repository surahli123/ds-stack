# Handoff prompt for Claude

Review the preserved local smoke failure at `docs/reports/2026-10-14-local-f1-smoke/` on base `b38292483163a55706fbefc5cfad6be06225e08c`. Start with README.md, parser-diagnostic.json, the unchanged readout.original.md, queries.jsonl, checks.jsonl, smoke-output.transcribed.txt, and TRACE-NOTES.md. The public execution trace and ledger provide retained command evidence and explicitly mark missing/raw-log redactions. Do not assume this documentation commit has been pushed; obtain the reported commit first.

Investigate and propose a consistent contract across eval/fixtures/f1/task.md, skills/ds-mode/SKILL.md (especially lines 89–91), eval/readout.py and eval/grade.py. The failure has two independent dimensions: localized parsing promotes a 95% confidence level to the headline estimate, and the task's causal-attribution question conflicts with the skill's measured-change headline instruction and the checker-displayed near-zero target. Preserve the distinction between observed total change (−2.0968 pp), adjusted within-segment change (−0.0023 pp), and an unidentifiable causal effect. A near-zero residual is not evidence of a zero causal effect.

Suggested fixes to evaluate, not changes already made:

1. Normalize supported Unicode punctuation/minus and localized units, and handle localized interval separators. Extract an estimate from an explicit field or unambiguous grammar; exclude confidence levels, dates and version identifiers. Do not silently choose a percent candidate when pp was required. Ambiguity or unit mismatch should produce a clear parse error.
2. Choose/document the supported language contract for alternatives, check labels and abstention. Either support localized labels deliberately or require canonical machine fields alongside localized prose. Avoid losing all alternatives silently.
3. Define separate measured-total, adjusted-descriptive and causal-estimand fields, or another explicit schema. Align task, skill and grader to the same declared estimand. Resolve the near-zero target through authorized evaluation ownership; do not change the preserved failed answer just to pass. Do not reveal gold to an analysis agent.
4. Resolve ds-mode's ds-doc dependency: install it safely in the runbook or make the standalone smoke path self-contained. Preserve existing user skills.
5. Distinguish source-query trace validation from semantic validation; ensure failed check attempts remain visible while corrected checks can be identified.

Regression acceptance criteria:

- The exact saved Chinese headline parses the estimate as −2.0968 pp and its interval as [−2.248, −1.946], never 95. English equivalents, ASCII/full-width parentheses, Unicode/ASCII minus, bold formatting and localized interval separators are tested.
- Confidence levels cannot become estimates. Missing or incompatible units and ambiguous multiple estimates fail explicitly; dates and v2 do not count as estimates.
- All five retained alternatives are represented or explicitly rejected under a documented language contract. No silent success with complete alternative loss. Coarse/fine checks and abstention handling have explicit tests.
- The task/skill/grader agree which estimand is assessed. A full-rollout readout may report measured decline and unidentifiable causality without being forced to assert zero causal impact. Descriptive residuals remain labeled descriptive.
- Safety and query/check provenance behavior remain intact; the malformed-spec record and corrected retry remain distinguishable. The original evidence directory remains immutable.
- Any future authorized regression or smoke run uses a new synthetic directory and reports a new result separately, never overwriting this failure. Keep gold inaccessible to analysis agents; only prescribed automated grading may load it after analysis completes.

No code has been fixed in this handoff. Do not use company data, DS_OVERLAY_DIR data or run SMA. Do not contact another agent or publish anything without the user's authorization. Explain proposed changes and validation separately from the preserved historical record.
