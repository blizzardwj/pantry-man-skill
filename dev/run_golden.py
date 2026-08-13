#!/usr/bin/env python3
"""L2 golden-case runner (manual executor for now).

Flow: setup fixture -> executor runs the prompt -> assert data state.

    python3 dev/run_golden.py --case add_inventory
    python3 dev/run_golden.py --all
    python3 dev/run_golden.py --all --no-wait   # skip the manual pause (assert current state)

Manual mode: after setup, the prompt is printed; you run it against any agent
(Hermes, Claude Code, Codex...) pointed at the temp agent home, then press Enter.
Future steps add automated executors behind the same interface.
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


def run_case(case, no_wait=False):
    case_id = case["id"]
    print(f"\n{'=' * 52}\ncase: {case_id}\n  prompt: {case['prompt']}")

    agent_home = Path(tempfile.mkdtemp(prefix="pantry_golden_"))
    data_dir = setup_fixture(case["fixture"], agent_home)
    print(f"  agent home: {agent_home}")
    print(f"  data dir:   {data_dir}")

    if not no_wait:
        input("\n  [manual] run the prompt against the agent at the temp home above, then press Enter...")

    results = []
    for target, assertions in case["assert"].items():
        f = target_path(agent_home, data_dir, target)
        if not f.exists():
            results.append((target, False, f"target file MISSING: {f}"))
            continue
        for ok_flag, msg in evaluate_file(f, assertions):
            results.append((target, ok_flag, msg))

    all_ok = True
    for target, ok_flag, msg in results:
        mark = "\u2705" if ok_flag else "\u274c"
        print(f"  {mark} [{target}] {msg}")
        all_ok = all_ok and ok_flag

    print(f"  -> {case_id}: {'PASS' if all_ok else 'FAIL'}")
    return all_ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", help="run one case by id")
    ap.add_argument("--all", action="store_true", help="run all cases")
    ap.add_argument("--no-wait", action="store_true", help="skip manual pause (assert current state)")
    args = ap.parse_args()

    if args.all:
        ids = sorted(p.stem for p in CASES_DIR.glob("*.json"))
    elif args.case:
        ids = [args.case]
    else:
        ap.print_help()
        sys.exit(1)

    all_ok = True
    for cid in ids:
        all_ok = run_case(load_case(cid), no_wait=args.no_wait) and all_ok
    print(f"\n{'=' * 52}\noverall: {'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
