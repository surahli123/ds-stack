#!/usr/bin/env python3
"""Generate the synthetic search-metric fixtures and their gold answers.

Deterministic: rerunning produces byte-identical databases and gold files.
Each fixture is a SQLite warehouse plus a task prompt written from the task
alone (the prompt never mentions the planted problem). Gold answers go to
eval/gold/, which is never copied into an agent's working directory.

    python3 eval/make_fixtures.py
"""

import json
import os
import random
import sqlite3
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
GOLD = os.path.join(HERE, "gold")

DAY_VOLUME = [1.00, 1.03, 0.98, 1.01, 0.97, 0.99, 1.02]
DAY_CTR = [1.000, 1.010, 0.990, 1.000, 1.005, 0.995, 1.000]
MIX_WORDS = ["mix", "composition", "platform share", "traffic share", "share shift", "simpson"]
RANKER_WORDS = ["ranker", "v2", "v3", "model"]


def days(start, n):
    first = date.fromisoformat(start)
    return [(first + timedelta(days=i)).isoformat() for i in range(n)]


def fresh_db(fixture_id):
    folder = os.path.join(FIXTURES, fixture_id)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "warehouse.db")
    if os.path.exists(path):
        os.remove(path)
    return folder, sqlite3.connect(path)


def write_task(folder, text):
    with open(os.path.join(folder, "task.md"), "w") as handle:
        handle.write(text.strip() + "\n")


def write_gold(fixture_id, gold):
    os.makedirs(GOLD, exist_ok=True)
    with open(os.path.join(GOLD, f"{fixture_id}.json"), "w") as handle:
        json.dump({"id": fixture_id, **gold}, handle, indent=2, sort_keys=True)
        handle.write("\n")


def ranker_fixture(fixture_id, start, ranker_old, ranker_new, weeks):
    """Two weeks of daily search aggregates by platform and country."""
    folder, conn = fresh_db(fixture_id)
    conn.execute("CREATE TABLE search_daily (date TEXT, platform TEXT, country TEXT, ranker TEXT, searches INTEGER, clicks INTEGER)")
    conn.execute("CREATE TABLE release_log (date TEXT, change TEXT)")
    dates = days(start, 14)
    countries = {"US": (0.55, 1.03), "other": (0.45, 0.965)}
    totals = {0: [0, 0], 1: [0, 0]}
    # Seeded day-level noise, so no week is an exact copy of another. A clean control
    # with byte-identical weeks reads as a stale-copy defect to a careful analyst.
    rng = random.Random(f"{fixture_id}-noise")
    for i, day in enumerate(dates):
        week = i // 7
        ranker = ranker_old if week == 0 else ranker_new
        for platform, (volume, ctr) in weeks[week].items():
            for country, (share, lift) in countries.items():
                searches = round(volume * DAY_VOLUME[i % 7] * share * rng.uniform(0.985, 1.015))
                clicks = round(searches * ctr * lift * DAY_CTR[i % 7] * rng.uniform(0.995, 1.005))
                conn.execute("INSERT INTO search_daily VALUES (?, ?, ?, ?, ?, ?)",
                             (day, platform, country, ranker, searches, clicks))
                totals[week][0] += searches
                totals[week][1] += clicks
    conn.execute("INSERT INTO release_log VALUES (?, ?)", (dates[7], f"ranker {ranker_new} rolled out to 100% of traffic"))
    conn.commit()
    conn.close()
    return folder, dates, totals


def ranker_prompt(dates, ranker_new):
    return f"""
Overall search CTR dropped week over week right after ranker {ranker_new} rolled out to 100% of traffic on {dates[7]}.
The PM thinks {ranker_new} caused the drop. Compare the week of {dates[0]} to {dates[6]} with the week of {dates[7]} to {dates[13]}.
How much of the change in overall CTR is attributable to {ranker_new}, in percentage points? This decides whether we roll it back.
"""


def make_mix_shift():
    weeks = [
        {"desktop": (60000, 0.36), "mobile": (40000, 0.22)},
        {"desktop": (45000, 0.36), "mobile": (55000, 0.22)},
    ]
    folder, dates, totals = ranker_fixture("f1", "2026-09-21", "v1", "v2", weeks)
    write_task(folder, ranker_prompt(dates, "v2"))
    overall = [100 * c / s for s, c in totals.values()]
    write_gold("f1", {
        "kind": "error",
        "planted": "mobile traffic share rose 40% -> 55%; within-platform CTR unchanged, so the drop is mix-shift and v2's effect is ~0",
        "unit": "pp",
        "accept_values": [{"value": 0.0, "tol": 0.3}],
        "estimand": "adjusted",
        "causal_identified": False,
        "accept_abstain": False,
        "must_rule_in": [MIX_WORDS],
        "must_not_rule_in": [RANKER_WORDS],
        "true_cause_words": MIX_WORDS,
        "naive_answer_pp": round(overall[1] - overall[0], 3),
    })


def make_clean_control():
    weeks = [
        {"desktop": (60000, 0.36), "mobile": (40000, 0.22)},
        {"desktop": (60000, 0.33), "mobile": (40000, 0.22)},
    ]
    folder, dates, totals = ranker_fixture("f3", "2026-08-31", "v2", "v3", weeks)
    write_task(folder, ranker_prompt(dates, "v3"))
    overall = [100 * c / s for s, c in totals.values()]
    delta = overall[1] - overall[0]
    write_gold("f3", {
        "kind": "clean",
        "planted": "nothing: platform mix is stable and desktop CTR fell after v3, so the whole drop is within-segment",
        "unit": "pp",
        "accept_values": [{"value": round(delta, 3), "tol": 0.3}],
        "estimand": "adjusted",
        "causal_identified": False,
        "accept_abstain": False,
        "must_rule_in": [],
        "must_not_rule_in": [MIX_WORDS],
        "true_cause_words": RANKER_WORDS + ["within"],
    })


def make_fanout():
    folder, conn = fresh_db("f2")
    conn.execute("CREATE TABLE query_stats (query_id INTEGER, week TEXT, searches INTEGER, clicks INTEGER)")
    conn.execute("CREATE TABLE query_labels (query_id INTEGER, intent TEXT, label_version INTEGER, is_current INTEGER)")
    nav = {"searches": 0, "clicks": 0}
    naive = {"searches": 0, "clicks": 0}
    for qid in range(1, 1001):
        searches = 50 + (qid * 37) % 200
        current = "navigational" if qid <= 400 else "informational"
        ctr = (0.55 if current == "navigational" else 0.25) + ((qid * 13) % 9 - 4) / 1000
        clicks = round(searches * ctr)
        conn.execute("INSERT INTO query_stats VALUES (?, '2026-W40', ?, ?)", (qid, searches, clicks))
        if 301 <= qid <= 600:
            old = "informational" if current == "navigational" else "navigational"
            conn.execute("INSERT INTO query_labels VALUES (?, ?, 1, 0)", (qid, old))
            conn.execute("INSERT INTO query_labels VALUES (?, ?, 2, 1)", (qid, current))
        else:
            conn.execute("INSERT INTO query_labels VALUES (?, ?, 1, 1)", (qid, current))
        labels = [current] + ([old] if 301 <= qid <= 600 else [])
        if current == "navigational":
            nav["searches"] += searches
            nav["clicks"] += clicks
        for label in labels:
            if label == "navigational":
                naive["searches"] += searches
                naive["clicks"] += clicks
    conn.commit()
    conn.close()
    write_task(folder, """
What was the click-through rate of navigational queries in week 2026-W40? Report it in percent.
Query intent labels are in query_labels. Marketing wants the number for a planning doc.
""")
    write_gold("f2", {
        "kind": "error",
        "planted": "300 queries were relabeled; old label rows remain (is_current = 0), so a join without the current-label filter counts stale labels",
        "unit": "percent",
        "accept_values": [{"value": round(100 * nav["clicks"] / nav["searches"], 3), "tol": 0.3}],
        "accept_abstain": False,
        "must_rule_in": [],
        "must_not_rule_in": [],
        "naive_answer_percent": round(100 * naive["clicks"] / naive["searches"], 3),
    })


def make_completeness():
    folder, conn = fresh_db("f4")
    conn.execute("CREATE TABLE search_hourly (date TEXT, hour INTEGER, searches INTEGER, clicks INTEGER)")
    dates = days("2026-09-30", 8)
    full = {"searches": 0, "clicks": 0}
    partial = {"searches": 0, "clicks": 0}
    same_hours = {"searches": 0, "clicks": 0}
    for i, day in enumerate(dates):
        last_hour = 10 if day == dates[-1] else 24
        for hour in range(last_hour):
            daytime = 8 <= hour <= 22
            searches = round((4200 if daytime else 1400) * DAY_VOLUME[i % 7])
            clicks = round(searches * (0.31 if daytime else 0.24))
            conn.execute("INSERT INTO search_hourly VALUES (?, ?, ?, ?)", (day, hour, searches, clicks))
            bucket = partial if day == dates[-1] else full
            bucket["searches"] += searches
            bucket["clicks"] += clicks
            if day != dates[-1] and hour < 10:
                same_hours["searches"] += searches
                same_hours["clicks"] += clicks
    conn.commit()
    conn.close()
    write_task(folder, f"""
Search CTR for yesterday ({dates[-1]}) looks down compared with the previous 7 days.
How big is the drop, in percentage points? Leadership wants the number this morning.
""")
    naive = 100 * partial["clicks"] / partial["searches"] - 100 * full["clicks"] / full["searches"]
    like_for_like = 100 * partial["clicks"] / partial["searches"] - 100 * same_hours["clicks"] / same_hours["searches"]
    write_gold("f4", {
        "kind": "abstain",
        "planted": f"{dates[-1]} has only hours 0-9 loaded; early hours have lower CTR, so the full-day comparison shows a fake drop",
        "unit": "pp",
        "accept_values": [{"value": round(like_for_like, 3), "tol": 0.3}],
        "accept_abstain": True,
        "must_rule_in": [],
        "must_not_rule_in": [],
        "naive_answer_pp": round(naive, 3),
    })


def make_srm():
    folder, conn = fresh_db("f5")
    conn.execute("CREATE TABLE experiment_daily (date TEXT, experiment TEXT, arm TEXT, users INTEGER, searches INTEGER, clicks INTEGER)")
    dates = days("2026-09-17", 14)
    arms = {"control": (35710, 0.300), "treatment": (34000, 0.312)}
    for i, day in enumerate(dates):
        for arm, (users, ctr) in arms.items():
            day_users = users + 10 * ((i % 3) - 1)
            searches = day_users * 6
            conn.execute("INSERT INTO experiment_daily VALUES (?, 'ranker_boost', ?, ?, ?, ?)",
                         (day, arm, day_users, searches, round(searches * ctr * DAY_CTR[i % 7])))
    conn.commit()
    conn.close()
    write_task(folder, f"""
Experiment ranker_boost ran a 50/50 split from {dates[0]} to {dates[-1]}.
Did treatment improve CTR? Give the lift in percentage points; it goes into the launch decision.
""")
    write_gold("f5", {
        "kind": "abstain",
        "planted": "assignment is about 51.2/48.8 against a planned 50/50 on every day and in total (sample ratio mismatch), so the lift is not trustworthy",
        "unit": "pp",
        "accept_values": [],
        "accept_abstain": True,
        "must_rule_in": [],
        "must_not_rule_in": [],
        "naive_answer_pp": 1.2,
    })


def make_definition_trap():
    """f6: the team's CTR definition (in the overlay's metrics.json) differs from the obvious one."""
    folder, conn = fresh_db("f6")
    conn.execute("CREATE TABLE search_daily_v (date TEXT, platform TEXT, traffic_type TEXT, searches INTEGER, "
                 "searches_with_results INTEGER, searches_with_click INTEGER, clicks INTEGER)")
    rng = random.Random("f6-noise")
    # per day and platform-half: searches, share with results, share of those with a click, clicks per clicking search
    traffic = {"external": (50000, 0.92, 0.50, 1.40), "internal": (2500, 0.96, 0.70, 1.50), "bot": (7500, 0.987, 0.02, 1.00)}
    dates = days("2026-10-05", 7)
    totals = {"governed": [0, 0]}
    for i, day in enumerate(dates):
        for platform in ("desktop", "mobile"):
            for kind, (volume, with_results, click_rate, per_click) in traffic.items():
                searches = round(volume * DAY_VOLUME[i] * rng.uniform(0.985, 1.015))
                results = round(searches * with_results)
                clicked = round(results * click_rate * rng.uniform(0.995, 1.005))
                clicks = round(clicked * per_click)
                conn.execute("INSERT INTO search_daily_v VALUES (?, ?, ?, ?, ?, ?, ?)",
                             (day, platform, kind, searches, results, clicked, clicks))
                if kind == "external":
                    totals["governed"][0] += results
                    totals["governed"][1] += clicked
    conn.commit()
    conn.close()
    overlay = os.path.join(folder, "overlay")
    os.makedirs(overlay, exist_ok=True)
    with open(os.path.join(overlay, "metrics.json"), "w") as handle:
        json.dump({"ctr": {
            "numerator": "searches_with_click",
            "denominator": "searches_with_results",
            "filters": ["traffic_type = 'external'"],
            "grain": "search",
            "source": "search_daily_v",
            "owner": "search analytics",
            "verified": "2026-10-01: matched the weekly business review dashboard to 0.1 pp",
            "pitfalls": ["clicks counts every click, so a search with three clicks counts three times",
                         "a search with no results shown is not in the denominator",
                         "bot and internal traffic are excluded"],
        }}, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_task(folder, f"""
What was search CTR for the week of {dates[0]} to {dates[-1]}, in percent?
It goes into the weekly business review.
""")
    write_gold("f6", {
        "kind": "error",
        "planted": "the team's CTR is searches_with_click / searches_with_results for external traffic (overlay metrics.json); clicks / searches over all traffic is about 8 points higher",
        "unit": "percent",
        "accept_values": [{"value": round(100 * totals["governed"][1] / totals["governed"][0], 3), "tol": 0.3}],
        "accept_abstain": False,
        "must_rule_in": [],
        "must_not_rule_in": [],
    })


def make_unanswerable():
    """f7: the question asks for purchases, which this warehouse doesn't log. The team's metric catalog (overlay)
    says so; the column name 'conversions' invites a substitute (they are add-to-cart events)."""
    folder, conn = fresh_db("f7")
    conn.execute("CREATE TABLE search_daily_c (date TEXT, searches INTEGER, clicks INTEGER, conversions INTEGER)")
    rng = random.Random("f7-noise")
    dates = days("2026-10-05", 7)
    for i, day in enumerate(dates):
        searches = round(120000 * DAY_VOLUME[i] * rng.uniform(0.985, 1.015))
        clicks = round(searches * 0.31 * rng.uniform(0.99, 1.01))
        conn.execute("INSERT INTO search_daily_c VALUES (?, ?, ?, ?)", (day, searches, clicks, round(searches * 0.083)))
    conn.commit()
    conn.close()
    overlay = os.path.join(folder, "overlay")
    os.makedirs(overlay, exist_ok=True)
    with open(os.path.join(overlay, "metrics.json"), "w") as handle:
        json.dump({
            "ctr": {"numerator": "clicks", "denominator": "searches", "filters": [], "grain": "search",
                    "source": "search_daily_c", "owner": "search analytics", "verified": "2026-10-01: matched the dashboard",
                    "pitfalls": []},
            "search_purchase_rate": {"available": False, "owner": "search analytics",
                                     "note": "purchases are logged only in the orders system, which this warehouse doesn't hold",
                                     "pitfalls": ["search_daily_c.conversions counts add-to-cart events, not purchases"]},
        }, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_task(folder, f"""
What share of searches in the week of {dates[0]} to {dates[-1]} led to a purchase, in percent?
Finance wants it for the quarterly model.
""")
    write_gold("f7", {
        "kind": "abstain",
        "planted": "purchases aren't logged here (overlay metric catalog); conversions are add-to-cart events, so any purchase rate is a substitute",
        "unit": "percent",
        "accept_values": [],
        "accept_abstain": True,
        "must_rule_in": [],
        "must_not_rule_in": [],
        "naive_answer_percent": 8.3,
    })


def make_many_to_many():
    """f8: a backfill loaded 250 high-CTR queries into query_category twice, so a join to the category double-counts them."""
    folder, conn = fresh_db("f8")
    conn.execute("CREATE TABLE query_week (query_id INTEGER, week TEXT, searches INTEGER, clicks INTEGER)")
    conn.execute("CREATE TABLE query_category (query_id INTEGER, category TEXT, loaded_at TEXT)")
    conn.execute("CREATE TABLE category_vertical (category TEXT, vertical TEXT)")
    conn.executemany("INSERT INTO category_vertical VALUES (?, ?)", [
        ("electronics", "shopping"), ("apparel", "shopping"), ("home", "shopping"), ("news", "info"), ("weather", "info")])
    shop = {"searches": 0, "clicks": 0}
    naive = {"searches": 0, "clicks": 0}
    for qid in range(1, 2001):
        searches = 40 + (qid * 29) % 160
        if qid <= 900:
            category = ("electronics", "apparel", "home")[qid % 3]
            ctr = 0.55 if qid > 650 else 0.30
        else:
            category, ctr = ("news", "weather")[qid % 2], 0.20
        clicks = round(searches * (ctr + ((qid * 7) % 11 - 5) / 1000))
        conn.execute("INSERT INTO query_week VALUES (?, '2026-W41', ?, ?)", (qid, searches, clicks))
        conn.execute("INSERT INTO query_category VALUES (?, ?, '2026-09-01')", (qid, category))
        copies = 1
        if 651 <= qid <= 900:
            conn.execute("INSERT INTO query_category VALUES (?, ?, '2026-10-09')", (qid, category))
            copies = 2
        if qid <= 900:
            shop["searches"] += searches
            shop["clicks"] += clicks
            naive["searches"] += searches * copies
            naive["clicks"] += clicks * copies
    conn.commit()
    conn.close()
    write_task(folder, """
What was the click-through rate in week 2026-W41 for queries in the shopping vertical, in percent?
Each query's category is in query_category, and category_vertical maps categories to verticals. Merchandising will cite it.
""")
    write_gold("f8", {
        "kind": "error",
        "planted": "a 2026-10-09 backfill loaded 250 high-CTR queries into query_category a second time, so a join counts them twice and inflates the rate",
        "unit": "percent",
        "accept_values": [{"value": round(100 * shop["clicks"] / shop["searches"], 3), "tol": 0.3}],
        "accept_abstain": False,
        "must_rule_in": [],
        "must_not_rule_in": [],
        "naive_answer_percent": round(100 * naive["clicks"] / naive["searches"], 3),
    })


def main():
    make_mix_shift()
    make_fanout()
    make_clean_control()
    make_completeness()
    make_srm()
    make_definition_trap()
    make_unanswerable()
    make_many_to_many()
    print(f"fixtures in {FIXTURES}, gold in {GOLD}")


if __name__ == "__main__":
    main()
