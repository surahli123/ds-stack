# Handover: finish the client_timestamp fix in load_events.py

## Current state
The daily job `load_events.py` has failed since Oct 6, so `events_daily` has no data for Oct 6, 7 and 8. Upstream renamed `client_ts` to `client_timestamp` that day, and our reader uses a fixed column list. The fix is half done on branch `fix/event-schema-mapping`: the mapping in `config/event_schema.yaml` and the reader side of `load_events.py` are updated, but the writer still uses the old name. The September backfill is complete and its row counts match the source.

## Next step
1. On `fix/event-schema-mapping`, change the writer in `load_events.py` to read the mapping from `config/event_schema.yaml` instead of the hardcoded `client_ts`.
2. Test against prod data once access is back (see Blockers).
3. Merge, then rerun `load_events.py` for Oct 6, 7 and 8.
4. Tell Sam the rerun is done, so the CTR dashboard stops showing the fake drop.

## Blockers and open questions
- Prod access: my access to the `prod-events` bucket expired on Oct 8. Renewal is requested from data platform as ticket DP-4412. Until it lands, the fix cannot be tested on prod data.
- Dashboard: the CTR dashboard reads `events_daily`, so it shows a drop for Oct 6-8 that is not real. Sam, the dashboard owner, already knows.

## Where things are
- Branch: `fix/event-schema-mapping`
- Mapping: `config/event_schema.yaml`
- Job: `load_events.py`
- Do not retry aliasing the column in SQL. It failed because the raw parquet files carry the new name and the reader takes a fixed schema list.
