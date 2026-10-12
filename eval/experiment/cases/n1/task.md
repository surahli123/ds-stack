You are the data scientist on a search ranking experiment, "Ranker v7". The launch review meets tomorrow.

Files in this directory:
- pulse.json: the Statsig Pulse results (Console API response), requested with {"cuped": "false", "confidence": "95"}
- experiment.json: the Statsig experiment config; audit_logs.json: its change history
- prereg.json: the pre-registration the team wrote before launch

Write the readout the launch review will read. It must start with one line, exactly:
Decision: <Ship | Don't ship | Escalate | Keep running | No effect found | Can't tell | Not an A/B test>
