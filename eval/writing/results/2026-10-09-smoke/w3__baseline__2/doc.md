# Handover: events pipeline fix (load_events.py)

## Summary
The daily job `load_events.py` has failed every day since Oct 6 with `KeyError 'client_ts'`. The upstream team renamed `client_ts` to `client_timestamp` in their schema on Oct 6 (confirmed in their changelog). As a result, `events_daily` has no data for Oct 6, 7 and 8. The fix is half done on a branch, and testing is blocked on prod access.

## Current state
- **Sep backfill (Sep 1-30):** complete. It was run with `backfill.py`, took about 6 hours, and row counts were validated against source. Nothing more to do.
- **Daily job:** failing since Oct 6, so Oct 6-8 are missing from `events_daily`.
- **Fix:** in progress on branch `fix/event-schema-mapping`.
  - `config/event_schema.yaml`: mapping updated (`client_ts` -> `client_timestamp`).
  - `load_events.py`: the reader now uses the mapping. The **writer still uses the old name** and needs finishing.
- **Prod access:** my access to the prod-events bucket expired. Renewal is requested from data platform in ticket **DP-4412** and is still pending. You may need your own access or need to chase the ticket.

## Why this approach
I first tried aliasing the column in the SQL. It didn't work: the raw parquet files already carry the new name, and the reader uses a fixed schema list. That attempt was reverted. The fixed list lives in `config/event_schema.yaml`. The right fix is to update the mapping there and make `load_events.py` read the mapping instead of its hardcoded list.

## Next steps
1. Finish the writer side of `load_events.py` so it uses the mapping instead of the old name.
2. Test against prod data once bucket access is available (DP-4412).
3. Merge `fix/event-schema-mapping`.
4. Rerun `load_events.py` for Oct 6, 7 and 8.
5. Tell Sam the data is restored (see below).

## Downstream impact
The CTR dashboard reads `events_daily`, so it shows a fake drop for Oct 6-8 until the rerun. Sam, the dashboard owner, has been told. Let Sam know once the backfill of those three days is done.

## Open items and caveats
- Nothing has been tested against prod data yet, so the reader change is unverified beyond the code itself.
- After the rerun, I suggest checking Oct 6-8 row counts against source, as was done for the Sep backfill.
