"""The agent end to end on the synthetic warehouse, with unittest only (the work laptop has
no pytest). Run from search_experiment_agent/:

    python3 -m unittest discover -s tests
"""

import copy
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "synth"))

import make_warehouse  # noqa: E402

from learning import cards, evaluate, knowledge, lessons  # noqa: E402
from search_agent import run as runner  # noqa: E402
from search_agent.m0 import checks as m0  # noqa: E402
from search_agent.m0.grade import grade  # noqa: E402
from search_agent.m1 import cuts  # noqa: E402
from search_agent.sources import config as cfgsrc  # noqa: E402
from search_agent.sources import resolver  # noqa: E402
from search_agent.sources import t1 as t1src  # noqa: E402
from search_agent.sources.warehouse import QueryRefused, SqliteWarehouse, bind, guard  # noqa: E402

FLIGHTS = ["synth-3p-boost-mid", "synth-typeahead-regress", "synth-auth-requery", "synth-answer-shift", "synth-null",
           "synth-split-loss", "synth-3p-boost-v2", "synth-3p-pin"]
STATE = {}


def setUpModule():
    tmp = tempfile.mkdtemp(prefix="agent-tests-")
    synth = os.path.join(tmp, "synth")
    make_warehouse.main(["--out", synth, "--flights", *FLIGHTS])
    overlay = os.path.join(tmp, "overlay")
    shutil.copytree(os.path.join(ROOT, "overlay.example"), overlay, ignore=shutil.ignore_patterns("contracts"))
    shutil.copytree(os.path.join(synth, "contracts"), os.path.join(overlay, "contracts"))
    STATE.update(tmp=tmp, synth=synth, overlay=overlay, gold=json.load(open(os.path.join(synth, "gold.json"))),
                 db=os.path.join(synth, "warehouse.sqlite"))


def tearDownModule():
    shutil.rmtree(STATE["tmp"], ignore_errors=True)


def run_flight(name, overlay=None, knowledge_dir=None, cards_dir=None, out=None):
    out = out or tempfile.mkdtemp(dir=STATE["tmp"])
    return runner.run(name, overlay or STATE["overlay"], SqliteWarehouse(STATE["db"]),
                      cfgsrc.JsonDirConfig(os.path.join(STATE["synth"], "configs")), out, knowledge_dir, cards_dir), out


def check(cid, status, affects=True):
    return {"id": cid, "name": m0.NAMES[cid], "status": status, "reason": f"{cid} {status}", "source": "test",
            "affects_grade": affects, "diagnosed_by": [], "details": {}}


class Grade(unittest.TestCase):
    """Every grade is reachable (this replaces the work repo's test that pinned the flags false)."""

    def test_four_grades(self):
        ok = [check("M0-1", "PASS"), check("M0-2", "PASS"), check("duration", "PASS")]
        self.assertEqual(grade(ok + [check("M0-2", "BLOCK")], False)["grade"], "not_permitted")
        self.assertEqual(grade(ok + [check("M0-3", "UNKNOWN")], False)["grade"], "directional_only")
        self.assertEqual(grade(ok, True)["grade"], "directional_only")
        self.assertEqual(grade(ok + [check("stratification", "UNKNOWN", affects=False)], False)["grade"], "decision_grade")
        warned = grade(ok + [check("M0-5", "WARN")], False)
        self.assertEqual((warned["grade"], len(warned["warns"])), ("decision_grade", 1))

    def test_stamp_needs_every_warning(self):
        result, out = run_flight("synth-3p-pin")
        self.assertIn("not yet approved", result["readout"])
        with self.assertRaises(ValueError):
            evaluate.stamp_readout(out, "owner", [])
        evaluate.stamp_readout(out, "owner", ["power"])
        self.assertIn("approved by owner", open(os.path.join(out, "readout.md")).read())


class M0(unittest.TestCase):
    def test_split_never_uses_metric_units(self):
        comparison = {"metrics": [{"metric": "Search Success Rate", "control_units": 5000, "test_units": 4000}]}
        cfg = {"groups": [{"name": "control", "size": 50}, {"name": "test", "size": 50}]}
        res = m0.split_check(comparison, cfg, {}, "control", "test", {}, split_metric=None)
        self.assertEqual(res["status"], "UNKNOWN")
        res = m0.split_check(comparison, {**cfg, "health_checks": [{"name": "Exposures are balanced", "status": "WARNING"}]},
                             {}, "control", "test", {}, split_metric=None)
        self.assertEqual((res["status"], res["source"]), ("WARN", "vendor health check"))

    def test_missing_config_is_unknown_not_block(self):
        res = m0.config_check(None, {}, None, "control", "test", "the config CLI")
        self.assertEqual(res["status"], "UNKNOWN")
        self.assertIn("the config CLI", res["reason"])

    def test_a_pass_needs_a_source(self):
        with self.assertRaises(ValueError):
            m0.result("M0-1", "PASS", "fine", None)


class Sources(unittest.TestCase):
    def test_guard_refuses_anything_but_one_read(self):
        for bad in ("DELETE FROM t", "SELECT 1; DROP TABLE t", "INSERT INTO t VALUES (1)", "PRAGMA x"):
            with self.assertRaises(QueryRefused):
                guard(bad)
        guard("WITH a AS (SELECT 'drop' AS x) SELECT x FROM a")

    def test_spark_binding_quotes_literals(self):
        sql, params = bind("SELECT * FROM t WHERE a = :a AND b IN :b", {"a": "it's", "b": ["x", "y"]}, "spark")
        self.assertEqual(sql, "SELECT * FROM t WHERE a = 'it''s' AND b IN ('x', 'y')")
        self.assertIsNone(params)

    def test_resolver(self):
        wh = SqliteWarehouse(STATE["db"])
        configs = cfgsrc.JsonDirConfig(os.path.join(STATE["synth"], "configs"))
        table, cols = "t1_scorecard", t1src.columns({})
        by_name = resolver.resolve("synth-null", configs, wh, table, cols)
        uuid = by_name["config_id"]
        self.assertEqual(resolver.resolve(uuid, configs, wh, table, cols)["experiment_name"], "synth-null")
        url = f"https://console.example/experiments/{uuid}/results"
        self.assertEqual(resolver.resolve(url, configs, wh, table, cols)["experiment_name"], "synth-null")
        no_config = resolver.resolve("synth-answer-shift", configs, wh, table, cols)
        self.assertIsNone(no_config["config"])
        with self.assertRaises(resolver.Unresolved):
            resolver.resolve("no-such-flight", configs, wh, table, cols)


class Cuts(unittest.TestCase):
    def test_cut_ties_to_t1(self):
        """A template with T1's definition (1P long clicks per full-page query, all tenants) gives T1's number."""
        wh = SqliteWarehouse(STATE["db"])
        wh_cfg = {**json.load(open(os.path.join(STATE["overlay"], "warehouse.json"))), "cohort": None}
        tpl = {"same_as_t1": {"produces": "1P long clicks per full-page query", "filter": "t.experience = 'surface_full'",
                              "x": "t.long_click_1p", "y": "1"}}
        as_of = wh.query("SELECT MAX(ds) AS d FROM t1_scorecard WHERE experiment_name = :e", {"e": "synth-null"})["rows"][0]["d"]
        res = cuts.run_cut(wh, "same_as_t1", tpl, wh_cfg, "synth-null", as_of, "control", ["test"], min_units=1)
        t1 = wh.query("SELECT relative_delta FROM t1_scorecard WHERE experiment_name = :e AND ds = :d AND "
                      "metric_name = '1P Long Click Rate'", {"e": "synth-null", "d": as_of})["rows"][0]["relative_delta"]
        self.assertAlmostEqual(100 * res["metrics"][0]["rel_delta"], t1, places=6)

    def test_spark_series_uses_datediff(self):
        templates = cuts.load_templates()
        wh_cfg = json.load(open(os.path.join(STATE["overlay"], "warehouse.json")))
        sql = cuts.dry_run_sql(templates["primary_by_exposure_day"], wh_cfg, "spark")
        self.assertIn("DATEDIFF(", sql)
        self.assertTrue(sql.endswith("LIMIT 0"))

    def test_unapproved_tables_are_access_gaps(self):
        overlay = os.path.join(STATE["tmp"], "overlay-no-t3")
        shutil.copytree(STATE["overlay"], overlay, dirs_exist_ok=True)
        cfg = json.load(open(os.path.join(overlay, "warehouse.json")))
        cfg["approved"] = ["t1"]
        json.dump(cfg, open(os.path.join(overlay, "warehouse.json"), "w"))
        result, _ = run_flight("synth-3p-boost-mid", overlay=overlay)
        self.assertEqual(result["counts"]["grades"], {"boost_15": "directional_only"})
        self.assertGreater(result["counts"]["access_gaps"], 0)
        self.assertEqual(result["counts"]["cuts_ran"], 0)
        self.assertIn("once its tables are approved", result["readout"])


class EndToEnd(unittest.TestCase):
    """Each synthetic flight gets its planted grade and mechanism, and every finding cites its data."""

    @classmethod
    def setUpClass(cls):
        cls.results = {name: run_flight(name) for name in FLIGHTS if name != "synth-3p-pin"}

    def test_grades_and_mechanisms(self):
        for name, (result, _) in self.results.items():
            gold = STATE["gold"][name]
            o = evaluate.outcome(result)
            with self.subTest(flight=name):
                self.assertIn(gold["grade"], {p["grade"] for p in o.values()})
                if name == "synth-3p-boost-v2":
                    self.assertEqual(evaluate.gold_score(o, gold), 0)  # the renamed metric hides it until a lesson maps it
                else:
                    self.assertEqual(evaluate.gold_score(o, gold), 2)

    def test_findings_cite_statements_in_the_trace(self):
        for name, (result, _) in self.results.items():
            statements = {r["statement_id"] for r in result["trace"]["receipt_records"] if r["statement_id"]}
            for c in result["trace"]["claim_records"]:
                if c["support_level"] == "confirmed":
                    with self.subTest(flight=name, claim=c["claim_id"]):
                        self.assertTrue(c["statement_ids"])
                        self.assertTrue(set(c["statement_ids"]) <= statements)
            self.assertEqual(result["counts"]["unsupported"], 0)

    def test_readout_order_and_no_internal_names(self):
        for name, (result, _) in self.results.items():
            body = result["readout"].split("\n---\n")[0]
            with self.subTest(flight=name):
                for word in ("packet", "seal", "receipt", "M0-"):
                    self.assertNotIn(word, body)
                order = [body.find(h) for h in ("## Before triage", "## Ask the engineer", "## Similar experiments")]
                self.assertEqual(order, sorted(order))
                self.assertTrue(body.splitlines()[0].startswith("# "))

    def test_blocked_flight_reads_no_movements(self):
        result, _ = self.results["synth-split-loss"]
        self.assertIn("not interpretable", result["readout"])
        self.assertNotIn("What moved:", result["readout"])
        self.assertEqual(result["counts"]["cuts_ran"], 0)

    def test_trace_records_the_grade_after_each_action(self):
        result, _ = self.results["synth-3p-boost-mid"]
        actions = result["trace"]["action_records"]
        self.assertTrue(actions)
        self.assertTrue(all(a.get("grade_after") for a in actions))
        self.assertTrue(any(a.get("diagnoses") for a in actions))


class Learning(unittest.TestCase):
    """The loop: propose, evaluate with source flights held out, approve, version, cards."""

    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.mkdtemp(dir=STATE["tmp"])
        cls.cases = os.path.join(cls.shared, "cases")
        empty = os.path.join(cls.shared, "knowledge")
        os.makedirs(empty)
        for name in ("synth-3p-boost-v2", "synth-3p-pin", "synth-null", "synth-typeahead-regress"):
            _, out = run_flight(name, knowledge_dir=empty)
            evaluate.freeze(out, cls.cases, STATE["gold"][name])

    def setUp(self):
        self.dir = tempfile.mkdtemp(dir=STATE["tmp"])
        self.k = os.path.join(self.dir, "knowledge")
        os.makedirs(self.k)

    def mapping(self, metric, family, source):
        return lessons.new("metric_mapping", {"family": family, "metric": metric}, [source], "test")

    def test_mapping_lesson_generalises_to_a_held_out_flight(self):
        import explain
        from search_agent import LIBRARY
        library = explain.load_library(self.k, base=LIBRARY)
        scorecard = json.load(open(os.path.join(self.cases, "synth-3p-boost-v2", "scorecard.json")))
        proposed = lessons.propose_mappings(scorecard, library, "synth-3p-boost-v2")
        self.assertEqual([p["change"] for p in proposed], [{"family": "p3_placement", "metric": "3P Top-1 Placement Rate"}])
        report = evaluate.evaluate(proposed[0], self.cases, STATE["overlay"], self.k, SqliteWarehouse(STATE["db"]))
        self.assertTrue(report["pass"], report["status"])
        self.assertEqual(report["improved"], ["synth-3p-pin"])
        self.assertEqual([c["case"] for c in report["fit_cases"]], ["synth-3p-boost-v2"])
        before = knowledge.version_hash(self.k)
        after = evaluate.approve(proposed[0], report, "owner", self.k, os.path.join(self.dir, "lessons"))
        self.assertNotEqual(before, after)
        with self.assertRaises(ValueError):
            evaluate.approve(proposed[0], report, "owner", self.k, os.path.join(self.dir, "lessons"))

    def test_a_harmful_lesson_regresses_and_fails(self):
        bad = self.mapping("Typeahead CTR", "latency", "synth-3p-boost-v2")
        report = evaluate.evaluate(bad, self.cases, STATE["overlay"], self.k, SqliteWarehouse(STATE["db"]))
        self.assertFalse(report["pass"])
        self.assertIn("synth-typeahead-regress", report["regressions"])
        with self.assertRaises(ValueError):
            evaluate.approve(bad, report, "owner", self.k, os.path.join(self.dir, "lessons"))

    def test_stubs_and_readout_rules_are_not_replayed(self):
        stub = lessons.propose_patterns([{"flight": f, "counts": {}, "claim_records": [
            {"metric": "X", "support_level": "none", "change": "rose 1%", "pair": "t"}]} for f in "abc"])
        self.assertEqual(len(stub), 1)
        self.assertFalse(evaluate.evaluate(stub[0], self.cases, STATE["overlay"], self.k)["pass"])
        rule = lessons.new("readout_rule", {"rule": "say the arm first"}, ["synth-null"], "test")
        self.assertIn("model-facing", evaluate.evaluate(rule, self.cases, STATE["overlay"], self.k)["status"])

    def test_only_confirmed_cards_are_cited(self):
        folder = os.path.join(self.dir, "cards")
        base = {"layer": "l2-ranking", "tags": ["3p"], "families_moved": ["p3_placement"], "name": "x"}
        cards.save(folder, {**base, "experiment_name": "a", "status": "drafted"})
        cards.save(folder, {**base, "experiment_name": "b", "status": "drafted"})
        cards.confirm(folder, "b", "cause", "lesson", "owner")
        cards.save(folder, {**base, "experiment_name": "b", "status": "drafted"})  # a draft never overwrites a confirmed card
        cited, drafts = cards.similar(cards.load(folder), "c", "l2-ranking", ["3p"], ["p3_placement"])
        self.assertEqual([c["experiment_name"] for c in cited], ["b"])
        self.assertEqual([d["experiment_name"] for d in drafts], ["a"])
        cited, _ = cards.similar(cards.load(folder), "b", "l2-ranking", ["3p"], ["p3_placement"])
        self.assertEqual(cited, [])


if __name__ == "__main__":
    unittest.main()
