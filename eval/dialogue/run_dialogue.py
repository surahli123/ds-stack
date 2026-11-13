#!/usr/bin/env python3
"""Replay development dialogues in isolated Claude Code sessions; review results manually."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from execution import classify  # noqa: E402
from run_arms import PASSTHROUGH_ENV  # noqa: E402

TOOLS = 'Bash,Read,Write,Edit,Glob,Grep,Task,Agent'
NOTES = {
    'direct': 'When asked to plan, frame, scope or brainstorm an analysis, read and follow .claude/skills/ds-plan/SKILL.md.\n',
    'mode': 'For this data analysis request, read and follow .claude/skills/ds-mode/SKILL.md.\n',
}


def install_skills(work, source, entry):
    names = ('ds-mode', 'ds-plan') if entry == 'mode' else ('ds-plan',)
    hashes = {}
    for name in names:
        src = source / name
        if not (src / 'SKILL.md').is_file():
            raise ValueError(f'Missing {src / "SKILL.md"}')
        dest = work / '.claude' / 'skills' / name
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        hashes[name] = {str(p.relative_to(dest)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(dest.rglob('*')) if p.is_file()}
    (work / 'CLAUDE.md').write_text(NOTES[entry], encoding='utf-8')
    return hashes


def read_trace(raw, work):
    """Record successful Read calls for this run's installed skills, in call order."""
    work = Path(work)
    calls, results = [], {}
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        for block in event.get('message', {}).get('content', []) if isinstance(event.get('message'), dict) else []:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'tool_use' and block.get('name') == 'Read':
                path = block.get('input', {}).get('file_path', '')
                for skill in ('ds-mode', 'ds-plan'):
                    if (work / path).resolve() == (work / '.claude' / 'skills' / skill / 'SKILL.md').resolve():
                        calls.append({'skill': skill, 'path': path, 'tool_use_id': block.get('id')})
            if block.get('type') == 'tool_result':
                results[block.get('tool_use_id')] = not block.get('is_error', False)
    return [c for c in calls if c['tool_use_id'] is not None and results.get(c['tool_use_id']) is True]


def routing_status(reads, entry):
    names = [r['skill'] for r in reads]
    if entry == 'mode':
        return 'observed' if 'ds-mode' in names and 'ds-plan' in names[names.index('ds-mode') + 1:] else 'unverified'
    return 'observed' if 'ds-plan' in names else 'unverified'


def parse(raw):
    session = reply = cost = usage = turns = error = None
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        session = session or event.get('session_id')
        if event.get('type') == 'result':
            reply, cost, usage, turns = (event.get(k) for k in ('result', 'total_cost_usd', 'usage', 'num_turns'))
            if event.get('is_error'):
                error = reply or event.get('subtype') or 'error'
    return session, reply, cost, usage, turns, error


def run_case(case, arm, model, dest, timeout, source=None, source_version=None):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    records, transcript, raw_parts = [], [], []
    hashes = {}
    run_root = os.environ.get('DS_RUN_ROOT')
    if run_root:
        Path(run_root).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ds-dialogue-', dir=run_root) as root:
        work, config = Path(root) / 'project', Path(root) / 'config'
        work.mkdir(); config.mkdir()
        if arm != 'baseline':
            if source is None:
                raise ValueError('skill source required')
            hashes = install_skills(work, Path(source), case['entry'])
        env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
        env.update(HOME=str(config), CLAUDE_CONFIG_DIR=str(config))
        session = None
        for index, turn in enumerate(case['turns'], 1):
            prompt = turn['text']
            cmd = ['claude', '-p', prompt, '--model', model, '--output-format', 'stream-json', '--verbose',
                   '--allowedTools', TOOLS, '--max-turns', '60']
            if session:
                cmd += ['--resume', session]
            turn_started = time.monotonic()
            try:
                proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
                raw, stderr, code = proc.stdout, proc.stderr, proc.returncode
            except subprocess.TimeoutExpired as exc:
                raw = exc.stdout.decode(errors='replace') if isinstance(exc.stdout, bytes) else (exc.stdout or '')
                stderr = exc.stderr.decode(errors='replace') if isinstance(exc.stderr, bytes) else (exc.stderr or '')
                code = 'timeout'
            except OSError as exc:
                raw, stderr, code = '', str(exc), 'launch_error'
            elapsed = time.monotonic() - turn_started
            got_session, reply, cost, usage, model_turns, error = parse(raw)
            status = classify(code, reply, stderr, error)
            if status == 'ok' and (not got_session or (session and got_session != session)):
                status = 'session_missing_or_changed'
            (dest / f'turn-{index:02d}.jsonl').write_text(raw, encoding='utf-8')
            (dest / f'turn-{index:02d}.stderr.log').write_text(stderr, encoding='utf-8')
            raw_parts.append(raw)
            records.append({'turn': index, 'exit': code, 'execution': status, 'session_id': got_session,
                            'seconds': elapsed, 'cost_usd': cost, 'usage': usage, 'model_turns': model_turns})
            transcript.append({'turn': index, 'origin': turn.get('origin', 'USER'), 'user': prompt, 'assistant': reply})
            if status != 'ok':
                break
            session = got_session
    reads = read_trace('\n'.join(raw_parts), work)
    costs = [r['cost_usd'] for r in records]
    usages = [r['usage'] for r in records]
    model_turn_counts = [r['model_turns'] for r in records]
    usage_keys = set().union(*(u.keys() for u in usages if isinstance(u, dict)))
    total_usage = {key: sum(u[key] for u in usages) if all(isinstance(u, dict) and isinstance(u.get(key), (int, float)) for u in usages) else None for key in sorted(usage_keys)} if all(isinstance(u, dict) for u in usages) else None
    meta = {'case': case['id'], 'arm': arm, 'model': model, 'entry': case['entry'],
            'source_version': source_version, 'skill_hashes': hashes, 'turns': records,
            'completed': len(records) == len(case['turns']) and all(r['execution'] == 'ok' for r in records),
            'seconds': time.monotonic() - started,
            'cost_usd': sum(costs) if costs and all(isinstance(c, (int, float)) for c in costs) else None,
            'usage': total_usage,
            'model_turns': sum(model_turn_counts) if model_turn_counts and all(isinstance(t, int) for t in model_turn_counts) else None,
            'read_trace': reads,
            'routing': routing_status(reads, case['entry']) if arm != 'baseline' else 'not_applicable'}
    (dest / 'transcript.json').write_text(json.dumps(transcript, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (dest / 'meta.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, help='case id in cases.json')
    parser.add_argument('--arm', choices=('baseline', 'current', 'candidate'), required=True)
    parser.add_argument('--current-ref', help='explicit git commit or ref for current arm, resolved and recorded')
    parser.add_argument('--skill-source', type=Path, help='candidate directory containing ds-plan/ and ds-mode/')
    parser.add_argument('--model', required=True)
    parser.add_argument('--out', type=Path, required=True, help='new result directory')
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args()
    cases = json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))
    case = next((c for c in cases if c['id'] == args.case), None)
    if case is None:
        parser.error('unknown case')
    if args.arm == 'current' and not args.current_ref:
        parser.error('--current-ref is required for current')
    if args.arm == 'candidate' and not args.skill_source:
        parser.error('--skill-source is required for candidate')
    with tempfile.TemporaryDirectory(prefix='ds-dialogue-source-') as temp:
        source, version = None, None
        if args.arm == 'current':
            version = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', '--verify', args.current_ref + '^{commit}'], text=True).strip()
            archive = subprocess.check_output(['git', '-C', str(ROOT), 'archive', version, 'skills/ds-mode', 'skills/ds-plan'])
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                tar.extractall(temp, filter='data')
            source = Path(temp) / 'skills'
        elif args.arm == 'candidate':
            source = args.skill_source.resolve()
            version = str(source)
        meta = run_case(case, args.arm, args.model, args.out, args.timeout, source, version)
    print(json.dumps({'completed': meta['completed'], 'routing': meta['routing'], 'out': str(args.out)}))
    return 0 if meta['completed'] else 2


if __name__ == '__main__':
    sys.exit(main())
