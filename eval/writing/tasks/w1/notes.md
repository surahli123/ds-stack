analysis notes - ctr drop after ranker v2 (oct 1-2)

started by pulling search_daily for the two weeks around the v2 launch (v2 went to 100% on sep 28). overall ctr wk1 30.4%, wk2 28.3%, so -2.1 pp. PM (dana) thinks v2 broke something, wants to know by thursday whether to roll back.

first checked if data was complete - all 14 days there, 4 rows per day (platform x country), row counts flat. ok.

tried splitting by country first. US 31.3 -> 29.2, other 29.3 -> 27.3. both down about 2 pp, so not a country thing. dead end.

then by platform. desktop ctr 36.0% both weeks. mobile 22.0% both weeks!! within platform nothing moved. but mobile share of searches went 40% -> 55%. mobile has lower ctr so overall drops. ran the mix decomposition: within-segment effect -0.0001 pp, mix effect -2.10 pp. basically 100% mix.

so v2 is not the cause as far as this data shows. it's the traffic shift.

asked around why mobile went up - growth said there might have been an app store feature that week, not confirmed. need growth to confirm.

caveats: no holdout, v2 went to everyone at once so this is before/after only. a small v2 effect (under ~0.3 pp) would be invisible. also only looked at ctr, not long clicks or reformulation rate. long clicks looked flat in a quick check but i didn't do it properly.

also wasted an hour because the dashboard ctr uses a different denominator (searches with results shown) than the table (all searches) - numbers differ by ~0.5 pp but the drop is the same in both. use the dashboard definition when reporting.

recommendation for dana: don't roll back v2. ask growth to confirm what drove the mobile traffic jump. if they want certainty on v2 itself, run a 5% holdout for two weeks.
