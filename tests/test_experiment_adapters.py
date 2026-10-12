"""Adapters turn Statsig exports and mapped CSVs into the canonical schema; stats helpers are exact."""

import math

import pytest

import adapters
import expstats

PULSE = {"message": "ok", "data": {"ds": "2026-09-15", "primaryMetrics": [
    {"metricID": "Successful Search Rate::ratio", "directionality": "increase", "absoluteChange": 0.0034,
     "absoluteConfidenceIntervalDelta": 0.0019, "percentChange": 0.81, "percentConfidenceIntervalDelta": 0.45,
     "testMean": 0.4234, "controlMean": 0.42, "testStd": 0.0007, "controlStd": 0.0007,
     "testUnits": 100500, "controlUnits": 100000, "pValue": 0.0004}],
    "secondaryMetrics": [
    {"metric_id": "Queries per user::mean", "directionality": "decrease", "value": 0.02,
     "confidence_interval_delta": 0.05, "percent_change": 0.4, "percent_confidence_interval_delta": 1.0,
     "p_value": 0.4}]}}


def test_pulse_reads_both_spellings_and_converts_percent_and_half_widths():
    card = adapters.statsig_pulse([PULSE], {"control": "c", "test": "t1", "cuped": "true", "confidence": "95"})
    primary, secondary = card["comparisons"][0]["metrics"]
    assert primary["metric"] == "Successful Search Rate" and primary["metric_type"] == "ratio"
    assert primary["listed_as"] == "primary" and secondary["listed_as"] == "secondary"
    assert math.isclose(primary["rel_delta"], 0.0081)
    assert [round(b, 6) for b in primary["rel_ci"]] == [0.0036, 0.0126]
    assert [round(b, 6) for b in primary["abs_ci"]] == [0.0015, 0.0053]
    assert secondary["abs_delta"] == 0.02 and [round(b, 4) for b in secondary["abs_ci"]] == [-0.03, 0.07]
    assert card["analysis"] == {"ci_level": 0.95, "cuped": True, "sequential": None,
                                "mc_correction": "none", "as_of": "2026-09-15"}


def test_pulse_reads_bound_objects_and_records_unknown_settings_as_none():
    record = {"metricName": "CTR", "metricID": "ctr::ratio", "percentChange": 1.0,
              "percentConfidenceInterval": {"lower": 0.2, "upper": 1.8}, "absoluteChange": 0.003,
              "confidenceInterval": {"lower": 0.001, "upper": 0.005}}
    card = adapters.statsig_pulse([{"data": {"primaryMetrics": [record], "secondaryMetrics": []}}])
    metric = card["comparisons"][0]["metrics"][0]
    assert [round(b, 6) for b in metric["rel_ci"]] == [0.002, 0.018] and metric["abs_ci"] == [0.001, 0.005]
    assert card["analysis"]["cuped"] is None and card["analysis"]["ci_level"] is None


def test_pulse_without_metrics_is_an_error():
    with pytest.raises(adapters.AdapterError):
        adapters.statsig_pulse([{"data": {"primaryMetrics": [], "secondaryMetrics": []}}])


def test_config_reads_groups_dates_settings_health_and_edits():
    experiment = {"data": {
        "id": "ranker_v7", "name": "Ranker v7", "hypothesis": "v7 raises successful searches",
        "idType": "userID", "layerID": "search_ranking", "allocation": 20, "controlGroupID": "g0",
        "groups": [{"id": "g0", "name": "Control", "size": 50, "parameterValues": {"model": "v6"}},
                   {"id": "g1", "name": "Test", "size": 50, "parameterValues": {"model": "v7"}}],
        "startTime": 1757894400000, "duration": 14, "defaultConfidenceInterval": "95",
        "sequentialTesting": False, "bonferroniCorrection": False,
        "primaryMetrics": [{"name": "successful_search_rate", "type": "ratio", "direction": "increase"}],
        "healthChecks": [{"type": "has_balanced_exposures", "name": "Exposures balanced", "status": "FAILED"}]}}
    logs = {"data": [{"actionType": "experiment_edit", "date": "2026-09-18", "changeLog": "allocation 20 -> 10",
                      "changes": {"allocation": {"old": 20, "new": 10}}}]}
    config = adapters.statsig_config(experiment, logs)
    assert config["start"] == "2025-09-15" and config["allocation_pct"] == 20
    assert config["groups"][1]["parameters"] == {"model": "v7"} and config["control_group"] == "g0"
    assert config["settings"]["ci_level"] == 0.95 and config["settings"]["bonferroni"] is False
    assert config["health_checks"][0]["status"] == "FAILED"
    assert config["edits"][0]["changes"]["allocation"]["new"] == 10


def test_mapped_csv_uses_the_column_map_and_reports_missing_columns(tmp_path):
    path = tmp_path / "export.csv"
    path.write_text("Metric,Variant,Lift %,Lift low %,Lift high %,P\n"
                    "ctr,treatment,1.2,0.4,2.0,0.003\n")
    column_map = {"metric": "Metric", "test_group": "Variant", "rel_delta": "Lift %", "rel_ci_lo": "Lift low %",
                  "rel_ci_hi": "Lift high %", "p_value": "P", "_percent_fields": ["rel_delta", "rel_ci_lo", "rel_ci_hi"]}
    card = adapters.mapped_csv(str(path), column_map)
    metric = card["comparisons"][0]["metrics"][0]
    assert card["comparisons"][0]["test_group"] == "treatment"
    assert math.isclose(metric["rel_delta"], 0.012) and [round(b, 4) for b in metric["rel_ci"]] == [0.004, 0.02]
    with pytest.raises(adapters.AdapterError, match="columns not in the export"):
        adapters.mapped_csv(str(path), {**column_map, "abs_delta": "Abs"})


def test_relative_lift_interval_and_power_helpers():
    lift, low, high, se = expstats.relative_lift(0.30, 0.001, 0.303, 0.001)
    assert math.isclose(lift, 0.01) and low < 0.01 < high
    assert math.isclose(se, 1.01 * math.sqrt((1 / 300) ** 2 + (1 / 303) ** 2), rel_tol=1e-9)
    assert math.isclose(expstats.achieved_mde(0.002), (1.959964 + 0.841621) * 0.002, rel_tol=1e-5)
    assert expstats.benjamini_hochberg([0.01, 0.04, 0.03, 0.2, 0.5]) == [0]
    assert expstats.benjamini_hochberg([0.001, 0.002, 0.04]) == [0, 1, 2]
    slope, _ = expstats.weighted_slope([1, 2, 3, 4], [0.02, 0.015, 0.01, 0.005], [0.003] * 4)
    assert math.isclose(slope, -0.005)
