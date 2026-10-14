# Trace preservation and redaction

Before grading or sanitization, all fresh job outputs were copied byte-for-byte to the private local archive `~/ds-acceptance-2026-10-13-2343-control/raw-results-before-grading/`. The original generated summary files were subsequently added to that archive. This archive is not published. artifact-manifest.json records original and published hashes for each result file. Original probe reply, controller logs and grading outputs remain in that control directory.

Published agent.log files retain rendered public user/assistant/native-command sections with original line spans, safe execution metadata, and all explicit error and `is not isolated` warning lines. Timestamped telemetry and its multiline continuations are excluded. Internal reasoning and unrelated records are not published. Home-directory paths become <HOME>; email and credential-shaped strings are redacted. Existing source truncation is not reconstructed. A raw log is not claimed to be a complete auditable structured transcript; the custom-agent harness has transcript:false and the grader reports isolation as unverified.

Result text and query/check files are preserved except any necessary personal-path redactions. No numbers or analysis conclusions were corrected. meta.json's command home path is redacted without changing execution statuses. Grade summaries and acceptance output have only privacy redactions, so they remain complete diagnostic outputs, not newly computed grades.

The probe script itself deletes its internal temporary agent log. Only its printed reply/PASS and outer stderr file were retained; no complete probe execution transcript is claimed. Controller preflight commands are documented in README and execution-status rather than presented as recovered raw recordings. No gold, credential files, raw telemetry or unrelated session records are included.

Publication check: git diff --cached --check reports original Markdown hard-break trailing spaces in three saved answers and their logs, plus final blank lines in grader output. These source-format warnings are preserved intentionally rather than rewriting historical output.
