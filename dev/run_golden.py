#!/usr/bin/env python3
"""L2 golden-case runner.

Subcommands:
  prepare <case_id>          setup fixture into a temp agent home; print JSON
                             {home, data_dir, delegation_prompt} to stdout
  assert  <case_id> --home H run assertions against the temp home
  run     <case_id>          manual: prepare + pause + assert
  run-all [--no-wait]        run every case (manual; skip pause with --no-wait)

Executors: the `prepare` output's delegation_prompt is self-contained — feed it
to any agent (Hermes delegate_task, `claude -p`, `codex exec`, or a human),
then run `assert --home <home>` to score the result.
"""

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CASES_DIR = REPO / "dev" / "golden_cases"
FIXTURES_DIR = REPO / "dev" / "fixtures"
DATA_SUBDIR = Path("pantry") / "data"

sys.path.insert(0, str(Path(__file__).parent / "lib"))
from assert_engine import evaluate_file


def load_case(case_id):
    p = CASES_DIR / f"{case_id}.json"
    if not p.exists():
        raise SystemExit(f"case not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def setup_fixture(fixture_name, agent_home):
    src = FIXTURES_DIR / fixture_name
    if not src.is_dir():
        raise SystemExit(f"fixture not found: {src}")
    data_dir = agent_home / DATA_SUBDIR
    data_dir.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*"):
        shutil.copy2(f, data_dir / f.name)
    return data_dir


def target_path(agent_home, data_dir, target):
    if target == "response.txt":
        return agent_home / "response.txt"
    return data_dir / target


def delegation_prompt(case, data_dir):
    return (
        "你是 pantry-man skill 的执行者。用 pantry-man-skill 的规则处理下面这条用户指令。\n\n"
        "【数据目录覆盖 — 必须遵守】\n"
        f"本任务中，skill 里所有 [AGENT_HOME]/pantry/data 路径一律替换为：{data_dir}\n"
        "不要读写默认 agent home 下的任何 pantry 数据。\n\n"
        "【skill 规则】\n"
        f"先读取 {REPO / 'SKILL.md'}，并按需读取 {REPO / 'references'} 下的文件，严格遵守其流程。\n\n"
        "【用户指令】\n"
        f"{case['prompt']}\n\n"
        "【完成标准】\n"
        f"- 数据只写到 {data_dir}，不碰其他路径\n"
        "- 最后用一两句话报告：改动了哪些文件、加了/改了什么数据"
    )


def run_assertions(case, agent_home):
    data_dir = agent_home / DATA_SUBDIR
    results = []
    for target, assertions in case["assert"].items():
        f = target_path(agent_home, data_dir, target)
        if not f.exists():
            results.append((target, False, f"target file MISSING: {f}"))
            continue
        for ok_flag, msg in evaluate_file(f, assertions):
            results.append((target, ok_flag, msg))
    return results


def report(case_id, results):
    all_ok = True
    for target, ok_flag, msg in results:
        mark = "\u2705" if ok_flag else "\u274c"
        print(f"  {mark} [{target}] {msg}")
        all_ok = all_ok and ok_flag
    print(f"  -> {case_id}: {'PASS' if all_ok else 'FAIL'}")
    return all_ok


def cmd_prepare(case_id):
    case = load_case(case_id)
    agent_home = Path(tempfile.mkdtemp(prefix="pantry_golden_"))
    data_dir = setup_fixture(case["fixture"], agent_home)
    out = {
        "case_id": case_id,
        "prompt": case["prompt"],
        "home": str(agent_home),
        "data_dir": str(data_dir),
        "delegation_prompt": delegation_prompt(case, data_dir),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_assert(case_id, home):
    case = load_case(case_id)
    ok = report(case_id, run_assertions(case, Path(home)))
    sys.exit(0 if ok else 1)


def cmd_run(case_id, no_wait=False):
    case = load_case(case_id)
    print(f"\n{'=' * 52}\ncase: {case_id}\n  prompt: {case['prompt']}")
    agent_home = Path(tempfile.mkdtemp(prefix="pantry_golden_"))
    data_dir = setup_fixture(case["fixture"], agent_home)
    print(f"  agent home: {agent_home}")
    print(f"  data dir:   {data_dir}")
    if not no_wait:
        input("\n  [manual] run the prompt against the agent, then press Enter...")
    ok = report(case_id, run_assertions(case, agent_home))
    sys.exit(0 if ok else 1)


def cmd_run_all(no_wait=False):
    ids = sorted(p.stem for p in CASES_DIR.glob("*.json"))
    all_ok = True
    for cid in ids:
        case = load_case(cid)
        print(f"\n{'=' * 52}\ncase: {cid}\n  prompt: {case['prompt']}")
        agent_home = Path(tempfile.mkdtemp(prefix="pantry_golden_"))
        setup_fixture(case["fixture"], agent_home)
        if not no_wait:
            input("\n  [manual] run the prompt against the agent, then press Enter...")
        all_ok = report(cid, run_assertions(case, agent_home)) and all_ok
    print(f"\n{'=' * 52}\noverall: {'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


def main():
    ap = argparse.ArgumentParser(description="L2 golden-case runner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_prep = sub.add_parser("prepare", help="setup fixture; print JSON {home, data_dir, delegation_prompt}")
    p_prep.add_argument("case_id")

    p_assert = sub.add_parser("assert", help="run assertions against a temp home")
    p_assert.add_argument("case_id")
    p_assert.add_argument("--home", required=True)

    p_run = sub.add_parser("run", help="manual: prepare + pause + assert")
    p_run.add_argument("case_id")
    p_run.add_argument("--no-wait", action="store_true")

    p_all = sub.add_parser("run-all", help="run every case (manual)")
    p_all.add_argument("--no-wait", action="store_true")

    args = ap.parse_args()
    if args.cmd == "prepare":
        cmd_prepare(args.case_id)
    elif args.cmd == "assert":
        cmd_assert(args.case_id, args.home)
    elif args.cmd == "run":
        cmd_run(args.case_id, no_wait=args.no_wait)
    elif args.cmd == "run-all":
        cmd_run_all(no_wait=args.no_wait)


if __name__ == "__main__":
    main()
