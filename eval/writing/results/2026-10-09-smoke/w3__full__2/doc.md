# Handover: events pipeline schema fix

## Current state

The daily job `load_events.py` has failed since Oct 6, so `events_daily` has no data for Oct 6, 7 and 8. Upstream renamed `client_ts` to `client_timestamp`, and our reader uses a fixed schema list that still has the old name. The fix is half done on branch `fix/event-schema-mapping`: the mapping is updated and the reader side of `load_events.py` is done, but the writer still uses the old name. The September backfill is complete and its row counts match the source.

## Next step

Finish the writer in `load_events.py` on `fix/event-schema-mapping` so it reads the column mapping from `config/event_schema.yaml` instead of the hardcoded list. Then test on prod data, merge, and rerun `load_events.py` for Oct 6, 7 and 8.

## Blockers and open questions

- Prod test is blocked. My access to the prod-events bucket expired, and renewal is requested in ticket DP-4412 with data platform. If you have your own access, you can test without waiting.
- The CTR dashboard reads `events_daily`, so it shows a fake drop for Oct 6-8 until the rerun. Sam, the dashboard owner, knows. Tell Sam when the rerun finishes.

Don't retry aliasing the column in the SQL. It fails because the raw parquet files already carry the new name and the reader checks columns against the fixed list.

## Where things are

- Branch: `fix/event-schema-mapping`
- Mapping: `config/event_schema.yaml`
- Job: `load_events.py`
- Upstream changelog: confirms the rename on Oct 6
