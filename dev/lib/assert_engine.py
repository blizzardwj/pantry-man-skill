"""Assertion engine for golden cases (pure, deterministic, zero LLM).

Evaluates assertions against agent-mutated data files after a golden case runs.
Two target kinds, inferred from file extension:
  - *.json -> structural assertions (path + predicate)
  - *.txt  -> text assertions (substring contains / not_contains)

Structural predicates (on a dot-separated `path` inside the JSON):
  contains      list[str]  every name present in the array (match by `name` field)
  not_contains  list[str]  no name present in the array
  record_exists dict       some array element satisfies all field-path == value checks
  field_equals  any        resolved value == expected
  count_gte     int        array length >= expected
  count_equals  int        array length == expected
"""

import json


class AssertionError(Exception):
    pass


def resolve_path(obj, path):
    """Resolve a dot-separated path inside a JSON object. Returns value or None."""
    if path == "$":
        return obj
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
            if cur is None:
                return None
        else:
            return None
    return cur


def _names(arr):
    if not isinstance(arr, list):
        return []
    out = []
    for x in arr:
        if isinstance(x, dict) and "name" in x:
            out.append(x["name"])
        elif isinstance(x, str):
            out.append(x)
    return out


def evaluate_json(data, assertion):
    """Evaluate one structural assertion dict. Returns (ok, message)."""
    path = assertion.get("path", "$")
    val = resolve_path(data, path)

    if "contains" in assertion:
        have = _names(val)
        missing = [w for w in assertion["contains"] if w not in have]
        return (not missing, f"{path} contains {assertion['contains']} (missing: {missing})")

    if "not_contains" in assertion:
        have = _names(val)
        hit = [w for w in assertion["not_contains"] if w in have]
        return (not hit, f"{path} not_contains {assertion['not_contains']} (found: {hit})")

    if "record_exists" in assertion:
        rows = val if isinstance(val, list) else []
        match = any(
            all(resolve_path(x, k) == v for k, v in assertion["record_exists"].items())
            for x in rows
        )
        return (match, f"{path} record_exists {assertion['record_exists']}")

    if "field_equals" in assertion:
        return (val == assertion["field_equals"], f"{path} == {assertion['field_equals']!r} (got {val!r})")

    if "count_gte" in assertion:
        n = len(val) if isinstance(val, list) else 0
        return (n >= assertion["count_gte"], f"{path} count >= {assertion['count_gte']} (got {n})")

    if "count_equals" in assertion:
        n = len(val) if isinstance(val, list) else 0
        return (n == assertion["count_equals"], f"{path} count == {assertion['count_equals']} (got {n})")

    raise AssertionError(f"unknown structural assertion: {assertion}")


def evaluate_text(text, assertion):
    """Evaluate a text assertion (contains/not_contains as substring)."""
    if "contains" in assertion:
        missing = [w for w in assertion["contains"] if w not in text]
        return (not missing, f"text contains {assertion['contains']} (missing: {missing})")
    if "not_contains" in assertion:
        hit = [w for w in assertion["not_contains"] if w in text]
        return (not hit, f"text not_contains {assertion['not_contains']} (found: {hit})")
    if "max_method_types" in assertion:
        methods = assertion["max_method_types"]["methods"]
        max_n = assertion["max_method_types"]["max"]
        found = [m for m in methods if m in text]
        return (len(found) <= max_n, f"text method types <= {max_n} (found {len(found)}: {found})")
    raise AssertionError(f"unknown text assertion: {assertion}")


def evaluate_file(path, assertions):
    """Evaluate all assertions for one target file. Returns list of (ok, message)."""
    text = path.read_text(encoding="utf-8")
    results = []
    if path.suffix == ".json":
        data = json.loads(text)
        for a in assertions:
            results.append(evaluate_json(data, a))
    else:
        for a in assertions:
            results.append(evaluate_text(text, a))
    return results
