# Handover: events pipeline schema fix

## Current state

The daily job `load_events.py` has failed every day since Oct 6, so `events_daily` has no data for Oct 6, 7 and 8. Upstream renamed `client_ts` to `client_timestamp` on Oct 6 (confirmed in their changelog), and the job dies with `KeyError: 'client_ts'`. The fix is half done on branch `fix/event-schema-mapping`: the column mapping and the reader side are updated, the writer still uses the old name. The September backfill is complete and its row counts match the source.

## Next step

Finish the writer side of `load_events.py` on `fix/event-schema-mapping`, so it reads the mapping from `config/event_schema.yaml` (`client_ts` -> `client_timestamp`) instead of the hardcoded schema list. Then test on prod data, merge, and rerun `load_events.py` for Oct 6, 7 and 8.

## Blockers and open questions

- Prod access: my access to the `prod-events` bucket expired on Oct 8. Renewal is requested from data platform in ticket DP-4412 and still pending. You may need your own access; check whether it is current before starting.
- Until the rerun, the CTR dashboard (reads `events_daily`) shows a fake drop for Oct 6-8. Sam, the dashboard owner, knows. Tell Sam when the rerun lands.

## Where things are

- Branch: `fix/event-schema-mapping`
- Mapping: `config/event_schema.yaml`
- Job: `load_events.py`

Do not alias the column in SQL: I tried and reverted it. The raw parquet files carry the new name and the reader uses a fixed schema list, so only the mapping change works.
