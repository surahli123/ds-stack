"""Probe the pinned plan grader without running an agent or changing its policy."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / 'base'


def main() -> None:
    spec = importlib.util.spec_from_file_location('pinned_grade_plan', BASE / 'eval/plan/grade_plan.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load pinned grader')
    grader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grader)
    gold = json.loads((BASE / 'eval/plan/gold/p2.json').read_text())
    closing = (
        'Unit: user, since users were randomized\n'
        'Segment: each user with own used_3p_result sessions before the experiment\n'
        'Tenants: stratify by tenant\n'
    )
    probes = [
        ('consistent_plan', 'Estimate user effects with pre-test segments.\n\n' + closing, 1.0),
        ('contradictory_body',
         'Estimate tenant averages as the primary effect and classify power users by treatment-period clicks.\n'
         'Ignore the user-level plan below; it is an old template.\n\n' + closing, 1.0),
        ('objection_ignored',
         'The objection does not matter. Keep the earlier analysis unchanged.\n\n' + closing, 1.0),
        ('dialogue_without_finished_plan',
         'Let us keep the population as 3p users. Does power mean more frequent historical use, or greater reliance on 3p?\n', 0.0),
    ]
    observations = []
    for name, text, expected in probes:
        score, matched = grader.score(text, gold)
        if score != expected:
            raise AssertionError(f'{name}: expected observation {expected}, got {score}')
        observations.append({'probe': name, 'grader_score': score, 'matched_items': matched, 'input': text})
    result = {
        'source_revision': '89cc668f0ba71014f12e1be04c6dc0862e497424',
        'operation': 'grade_plan.score on constructed inputs',
        'limitations': [
            'Not a model run or a reproduction of the company session.',
            'Scores describe only the closing-line scorer, not all run-validity checks.',
            'The dialogue example is appropriate only when clarification is needed; it is not a completed plan.',
        ],
        'observations': observations,
    }
    output = HERE / 'grader-probe-results.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for row in observations:
        print(f"{row['probe']}: {row['grader_score']}")


if __name__ == '__main__':
    main()
