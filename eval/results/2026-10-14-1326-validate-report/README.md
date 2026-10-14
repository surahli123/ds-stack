# Small Codex validation
Commit: 5eab0bb34c9551d9eb87696e17190ad8fa58dce1. Codex CLI 0.153.4; gpt-6-astra; reasoning effort none.
V1: 251 passed in 3.38s. Published English and Chinese replay INVALID; exit 2; expected failure counts matched. Existing /tmp/ds-replay matched all 1759 archived files byte-for-byte and was preserved.
V2: only .system; marker and imagegen, openai-docs, plugin-creator, review-agent, skill-creator, skill-installer.
V3: PASS. SKILLS: imagegen, openai-docs, plugin-creator, skill-creator, skill-installer. INSTRUCTIONS: NONE.
V4: exit 2; not_isolated 1; Codex not started because ds-canary was present; elapsed 0.0s. Canary removed.
V5: exit 0; executed 4 of 4; failed none; not started 0. All one attempt: f1 baseline 61.6s; f1 full 93.2s; f6 baseline 91.4s; f6 full 79.4s.
V6: originals restored before grading. Plumbing PASS (2 of 2 full runs). Canary INVALID expected. Other levels are not acceptance results for this small set. Complete grading output in grading.txt.
Raw synthetic artifacts are retained locally under ~/ds-acceptance-2026-10-14-1326-control/raw-results-before-grading/. Public logs contain only metadata and errors with source line numbers; internal reasoning, telemetry and tool transcripts are omitted. Home paths and identifying strings redacted. SHA-256 hashes provide traceability. No retries were needed; no attempt logs exist.
Preserved ungraded contaminated directories: eval/results/2026-10-14-codex-en and eval/results/2026-10-14-codex-zh.
No full matrix, SMA, implementation edits, criteria edits or skill edits performed.
