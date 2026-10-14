## Answer
Headline: 36.97 % (95% CI 36.68 to 37.26)
Shopping-vertical click-through rate in 2026-W41 was 36.97%, which is 39,857 clicks on 107,810 searches across 900 queries.
- Observed: 36.97 % (36.68 to 37.26). This is clicks divided by searches. The interval is a binomial approximation. [measured]
- Adjusted: not computed (the question asks for a single-week level, so there is nothing to adjust)
- Causal effect: not identified (this is a descriptive rate, with no intervention or comparison)

## What it means for merchandising
This is a reporting figure, so no decision threshold applies. The interval is about ±0.3 points wide, so quote it as roughly 37.0%. Any comparison needs a change bigger than that.

## Why we believe it
- Alternatives considered:
  - Joining query_category to the data as-is: ruled out. 250 queries have a duplicate category row from a 2026-10-09 reload, with the same category, so a plain join double-counts them. That join gives 40.90%, which is wrong. [measured]
  - Averaging the per-query CTRs: ruled out. It gives 36.94%, close to the pooled figure, but the pooled rate is the standard CTR. [measured]
  - Category changes between the two loads: ruled out. No query has more than one distinct category. [measured]
- Checks run:
  - Category duplicates: flag. 2,250 rows cover 2,000 distinct queries, and I deduplicated them.
  - Coverage: pass. All 2,000 W41 queries have a category, and each appears once in query_week.
  - Data quality: pass. There are no null values and no row has clicks above searches.
  - Interval: flag. It treats searches as independent, so it ignores clustering by query and is probably slightly too narrow.

## Caveats, and what would change the answer
- The CTR definition (clicks ÷ searches, pooled) is assumed. No metrics.json was present.
- If merchandising defines the shopping vertical differently, the number changes. I used electronics, apparel and home, per category_vertical.
- The data holds only W41, so I could not compare it with other weeks or check whether W41 is complete.
- The duplicate rows in query_category should be fixed upstream. Anyone who joins the table directly will get 40.9%.

## Provenance
- Metric: sum(clicks) / sum(searches), pooled, from stated here [guess]
- Data: query_week, query_category (deduplicated) and category_vertical, week 2026-W41 (the only week present)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: run inline in Python/sqlite3; not saved to a file.