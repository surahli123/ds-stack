You are the data scientist on a search ranking experiment, "Ranker v7". The engineer who ran it presents it at the triage meeting tomorrow. Triage reads the scorecard and asks the engineer why each metric moved.

Files in this directory:
- pulse.json: the Statsig Pulse results (Console API response), requested with {"cuped": "false", "confidence": "95"}
- experiment.json: the Statsig experiment config; audit_logs.json: its change history
- prereg.json: the pre-registration the team wrote before launch

Prepare the engineer for triage: say why the metrics moved, which deep-dive cuts to run next and what each would show, and whether the results are ready for triage. Your reply must contain one line, exactly:
Ready for triage: <Ready | Ready, with open questions | Not ready>
