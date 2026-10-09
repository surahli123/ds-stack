# Handover: events pipeline fix (`client_ts` rename)

## Summary
The daily job `load_events.py` has failed since Oct 6 with `KeyError 'client_ts'`. Upstream renamed the column to `client_timestamp` on Oct 6 (confirmed in their changelog). The fix is half done on branch `fix/event-schema-mapping`. It is blocked on prod bucket access (ticket DP-4412).

## Current state
- **September backfill (`backfill.py`):** complete. It covered Sep 1–30 and took about 6 hours. Row counts were validated against source and all match. Nothing more to do.
- **Daily job:** failing since Oct 6, so `events_daily` has no data for Oct 6, 7 and 8.
- **Fix:** in progress on `fix/event-schema-mapping`.
  - `config/event_schema.yaml`: mapping updated (`client_ts` -> `client_timestamp`). Done.
  - `load_events.py` reader: now reads the mapping instead of the hardcoded list. Done.
  - `load_events.py` writer: still uses the old name `client_ts`. **Not done.**
- **Testing:** not tested against prod. My access to the `prod-events` bucket expired on Oct 8. I requested renewal from data platform (DP-4412) and it was still pending when I stopped.

## Next steps
1. Finish the writer side of `load_events.py` so it uses the mapping and the new column name.
2. Check whether DP-4412 is resolved. If it isn't, chase data platform.
3. Test the branch against prod data.
4. Merge the branch.
5. Rerun `load_events.py` for Oct 6, 7 and 8, then check that `events_daily` has rows for those dates.

## Downstream impact
The CTR dashboard reads `events_daily`. It shows a fake drop for Oct 6–8 until the rerun. I've told the dashboard owner, Sam. Let Sam know once the data is backfilled.

## What not to retry
Aliasing the column in the SQL does not work. The raw parquet files already use the new name, and the reader uses a fixed schema list, so the alias never takes effect. I reverted that attempt. The right fix is the config mapping approach above.
