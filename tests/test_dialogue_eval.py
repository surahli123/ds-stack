import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('dialogue_runner', ROOT / 'eval/dialogue/run_dialogue.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_replay_is_incremental_and_resumes_and_preserves_unknown_usage(tmp_path, monkeypatch):
    bindir = tmp_path / 'bin'
    bindir.mkdir()
    claude = bindir / 'claude'
    claude.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
prompt = args[args.index('-p') + 1]
resume = args[args.index('--resume') + 1] if '--resume' in args else None
assert resume == ('session-1' if Path('seen').exists() else None)
assert not Path('gold').exists() and not Path('rubric').exists()
assert ('SECOND SECRET' not in prompt) if resume is None else ('FIRST SECRET' not in prompt)
Path('seen').write_text('yes')
print(json.dumps({'type':'system','session_id':'session-1'}))
print(json.dumps({'type':'result','session_id':'session-1','result':'answer', 'total_cost_usd': 0 if resume else None, 'usage': {'input_tokens': 0} if resume else None}))
''')
    claude.chmod(0o755)
    monkeypatch.setenv('PATH', str(bindir))
    # Use an absolute interpreter in the fake executable's shebang.
    claude.write_text(claude.read_text().replace('/usr/bin/env python3', __import__('sys').executable))
    case = {'id': 'sample', 'entry': 'direct', 'turns': [{'text':'FIRST SECRET'}, {'text':'SECOND SECRET'}]}
    meta = runner.run_case(case, 'baseline', 'test', tmp_path / 'out', 10)
    assert meta['completed'] and len(meta['turns']) == 2
    assert meta['turns'][1]['session_id'] == 'session-1'
    assert meta['turns'][0]['usage'] is None and meta['turns'][1]['usage'] == {'input_tokens': 0}
    assert meta['cost_usd'] is None
    transcript = json.loads((tmp_path / 'out/transcript.json').read_text())
    assert [t['user'] for t in transcript] == ['FIRST SECRET', 'SECOND SECRET']
    assert all(t['assistant'] == 'answer' for t in transcript)


def test_failure_stops_before_followup(tmp_path, monkeypatch):
    bindir = tmp_path / 'bin'; bindir.mkdir()
    cli = bindir / 'claude'
    cli.write_text(f'#!{__import__("sys").executable}\nimport json\nprint(json.dumps({{"type":"result", "session_id":"s", "is_error":True, "result":"refused"}}))\n')
    cli.chmod(0o755); monkeypatch.setenv('PATH', str(bindir))
    case = {'id':'failure', 'entry':'direct', 'turns':[{'text':'first'}, {'text':'second'}]}
    meta = runner.run_case(case, 'baseline', 'test', tmp_path / 'out', 10)
    assert not meta['completed'] and len(meta['turns']) == 1


def test_install_source_and_read_trace(tmp_path):
    source = tmp_path / 'skills'
    for skill in ('ds-mode', 'ds-plan'):
        (source / skill).mkdir(parents=True)
        (source / skill / 'SKILL.md').write_text(skill + ' candidate')
    work = tmp_path / 'work'; work.mkdir()
    installed = runner.install_skills(work, source, 'mode')
    assert set(installed) == {'ds-mode', 'ds-plan'}
    assert 'ds-mode' in (work / 'CLAUDE.md').read_text()
    assert 'ds-plan' not in (work / 'CLAUDE.md').read_text()
    events = []
    for s in ('ds-mode', 'ds-plan'):
        events += [{'type':'assistant','message':{'content':[{'type':'tool_use','id':s,'name':'Read','input':{'file_path': str(work / '.claude' / 'skills' / s / 'SKILL.md')}}]}}, {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':s,'content':'skill'}]}}]
    raw = '\n'.join(json.dumps(e) for e in events)
    reads = runner.read_trace(raw, work)
    assert [r['skill'] for r in reads] == ['ds-mode', 'ds-plan']
    assert runner.routing_status(reads, 'mode') == 'observed'
    assert runner.routing_status(reads[1:], 'mode') == 'unverified'
    assert runner.read_trace(raw.replace(str(work), str(work) + '-other'), work) == []
    assert [r['skill'] for r in runner.read_trace(raw.replace(str(work) + '/', ''), work)] == ['ds-mode', 'ds-plan']


def test_current_ref_and_candidate_install_distinct_sources(tmp_path, monkeypatch):
    import subprocess
    import sys
    bindir = tmp_path / 'bin'; bindir.mkdir()
    cli = bindir / 'claude'
    cli.write_text(f'''#!{sys.executable}
import json
from pathlib import Path
plan = Path('.claude/skills/ds-plan/SKILL.md').read_text()
mode = Path('.claude/skills/ds-mode/SKILL.md').read_text()
print(json.dumps({{'type':'result', 'session_id':'same', 'result':plan[:40] + mode[:40]}}))
''')
    cli.chmod(0o755)
    # Git is needed for current source, while fake Claude is first on PATH.
    monkeypatch.setenv('PATH', str(bindir) + ':' + __import__('os').environ['PATH'])
    commit = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    candidate = tmp_path / 'candidate-source'
    for name in ('ds-mode', 'ds-plan'):
        (candidate / name).mkdir(parents=True)
        (candidate / name / 'SKILL.md').write_text('candidate ' + name)
    for arm in ('current', 'candidate'):
        args = ['run_dialogue.py', '--case', 'mode-entry', '--arm', arm, '--model', 'fake', '--out', str(tmp_path / arm)]
        args += ['--current-ref', commit] if arm == 'current' else ['--skill-source', str(candidate)]
        monkeypatch.setattr(sys, 'argv', args)
        assert runner.main() == 0
    current = json.loads((tmp_path / 'current/meta.json').read_text())
    modified = json.loads((tmp_path / 'candidate/meta.json').read_text())
    assert current['source_version'] == commit
    assert current['skill_hashes']['ds-plan'] != modified['skill_hashes']['ds-plan']
    assert current['routing'] == modified['routing'] == 'unverified'
    assert 'candidate ds-plan' in json.loads((tmp_path / 'candidate/transcript.json').read_text())[0]['assistant']


def test_failed_read_is_not_routing_evidence():
    events = [
        {'type':'assistant', 'message':{'content':[{'type':'tool_use','id':'x','name':'Read','input':{'file_path':'.claude/skills/ds-plan/SKILL.md'}}]}},
        {'type':'user', 'message':{'content':[{'type':'tool_result','tool_use_id':'x','is_error':True,'content':'not found'}]}}
    ]
    assert runner.read_trace('\n'.join(json.dumps(e) for e in events), Path.cwd()) == []


def test_cases_file_records_exact_input_and_hashes_outside_workspace(tmp_path, monkeypatch):
    import hashlib
    import sys

    bindir = tmp_path / 'bin'; bindir.mkdir()
    cli = bindir / 'claude'
    cli.write_text(f'''#!{sys.executable}
import json
from pathlib import Path
assert not list(Path('.').rglob('validation-cases.json'))
assert not list(Path('.').rglob('validation-rubric.md'))
print(json.dumps({{'type':'result', 'session_id':'s', 'result':'ok'}}))
''')
    cli.chmod(0o755)
    monkeypatch.setenv('PATH', str(bindir))
    case = {'id': 'external', 'entry': 'direct', 'turns': [{'origin': 'USER', 'text': 'A'}, {'origin': 'USER', 'text': 'B'}]}
    case_file = tmp_path / 'validation-cases.json'
    raw = json.dumps([case], ensure_ascii=False, indent=2).encode() + b'\n'
    case_file.write_bytes(raw)
    monkeypatch.setattr(sys, 'argv', ['run_dialogue.py', '--case', 'external', '--cases-file', str(case_file), '--arm', 'baseline', '--model', 'fake', '--out', str(tmp_path / 'out')])
    assert runner.main() == 0
    case_file.write_text('changed')
    meta = json.loads((tmp_path / 'out/meta.json').read_text())
    assert meta['case_input'] == case
    canonical = json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    assert meta['case_input_sha256'] == hashlib.sha256(canonical).hexdigest()
    assert meta['cases_file_sha256'] == hashlib.sha256(raw).hexdigest()


def test_replay_pins_budget_and_effort_and_keeps_clean_config(tmp_path, monkeypatch):
    import sys

    bindir = tmp_path / 'bin'; bindir.mkdir()
    cli = bindir / 'claude'
    cli.write_text(f'''#!{sys.executable}
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
assert os.environ['HOME'] != {str(tmp_path / 'login-home')!r}
assert os.environ['CLAUDE_CONFIG_DIR'] != {str(tmp_path / 'login-config')!r}
assert Path(os.environ['HOME']).is_dir()
assert os.environ['HOME'] == os.environ['CLAUDE_CONFIG_DIR']
assert '--safe-mode' not in args
assert args[args.index('--max-budget-usd') + 1] == '0.35'
assert args[args.index('--effort') + 1] == 'medium'
assert Path('.claude/skills/ds-plan/SKILL.md').read_text() == 'run-specific plan'
print(json.dumps({{'type':'result', 'session_id':'s', 'result':'ok'}}))
''')
    cli.chmod(0o755)
    monkeypatch.setenv('PATH', str(bindir))
    monkeypatch.setenv('HOME', str(tmp_path / 'login-home'))
    monkeypatch.setenv('CLAUDE_CONFIG_DIR', str(tmp_path / 'login-config'))
    source = tmp_path / 'source'
    (source / 'ds-plan').mkdir(parents=True)
    (source / 'ds-plan/SKILL.md').write_text('run-specific plan')
    case = {'id':'safe', 'entry':'direct', 'turns':[{'text':'first'}, {'text':'finish'}]}
    meta = runner.run_case(case, 'candidate', 'test', tmp_path / 'out', 10, source,
                           turn_budget_usd=0.35, effort='medium')
    assert meta['completed']
    assert meta['turn_budget_usd'] == 0.35 and meta['effort'] == 'medium'
