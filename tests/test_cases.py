"""Test cases: input, expected result, actual result, pass or fail.

Run from the project folder:
    python tests/test_cases.py        writes results/test_cases.csv
    pytest tests/test_cases.py        runs the same cases under pytest

Expected results were written before the first run.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src import skill_input as si  # noqa: E402
from src.matcher import RoleMatcher  # noqa: E402

MATCHER = RoleMatcher()
SKILLS = si.load_skills()
SYNONYMS = si.load_synonyms()


def analyze(selected, typed):
    """Same steps as the screen: clean input, then match."""
    student, unrecognized = si.combine(selected, typed, SKILLS, SYNONYMS)
    return student, unrecognized, MATCHER.recommend(student, top_n=3)


def roles_of(results):
    return [r["role"] for r in results]


# Each case returns (actual_text, passed).
def t_empty():
    s, u, r = analyze([], "")
    return f"skills={s}, results={r}", s == [] and r == []


def t_none_selected():
    s, u, r = analyze([], "   ")
    return f"skills={s}, results={r}", s == [] and r == []


def t_none_type():
    s, u, r = analyze(None, None)
    return f"skills={s}, results={r}", s == [] and r == []


def t_one_skill():
    s, u, r = analyze(["python"], "")
    ok = len(r) == 3 and all(0 < x["score"] <= 1 for x in r)
    return f"{[(x['role'], x['score']) for x in r]}", ok


def t_all_skills():
    s, u, r = analyze(SKILLS, "")
    ok = len(r) == 3 and all(0 < x["score"] <= 1 for x in r)
    return f"{len(s)} skills, top3={[(x['role'], x['score']) for x in r]}", ok


def t_misspelled():
    s, u, r = analyze([], "pythno, javascrpit, postgre sql")
    return f"skills={s}, unrecognized={u}", s[:2] == ["python", "javascript"]


def t_synonym_py():
    s, u, r = analyze([], "py")
    return f"skills={s}", s == ["python"]


def t_synonym_multi():
    s, u, r = analyze([], "ms sql, node, oop")
    ok = s == ["microsoft sql server", "node.js", "object-oriented programming"]
    return f"skills={s}", ok


def t_duplicates():
    s, u, r = analyze(["python", "python"], "Python, py, PYTHON")
    return f"skills={s}", s == ["python"]


def t_special_only():
    s, u, r = analyze([], "@@@, ###, !!!, $$$")
    return f"skills={s}, results={r}", s == [] and r == []


def t_special_mixed():
    s, u, r = analyze([], "  PYTHON!!! ; <script>alert(1)</script>")
    return f"skills={s}, unrecognized={u}", s == ["python"]


def t_case_space():
    s, u, r = analyze([], "   PyThOn   ,   SQL ")
    return f"skills={s}", s == ["python", "sql"]


def t_unknown_skill():
    s, u, r = analyze([], "quantum basket weaving")
    return f"skills={s}, unrecognized={u}", s == [] and r == [] and u == ["quantum basket weaving"]


def t_generic_skills():
    s, u, r = analyze(["teamwork", "communication", "problem solving"], "")
    top = r[0]["score"] if r else None
    # Skills shared by many roles should not give a strong match to any one role.
    return f"top3={[(x['role'], x['score']) for x in r]}", len(r) == 3 and top < 0.5


def t_long_input():
    s, u, r = analyze([], "python, " * 2000)
    return f"skills={s}", s == ["python"]


def t_security_profile():
    s, u, r = analyze(["penetration testing", "siem", "incident response"], "")
    return f"top1={r[0]['role']}", r[0]["role"] == "Cybersecurity Analyst"


def t_web_profile():
    s, u, r = analyze(["html", "css", "react", "bootstrap", "responsive design"], "")
    return f"top1={r[0]['role']}", r[0]["role"] == "Web Developer"


def t_network_profile():
    s, u, r = analyze(["vlan", "routing", "switching", "cisco ios", "subnetting"], "")
    return f"top1={r[0]['role']}", r[0]["role"] == "Network Administrator"


def t_idf_weight():
    # "teamwork" is in all 8 roles, "penetration testing" in one. The rare skill
    # must carry the larger TF-IDF weight.
    w = MATCHER.role_weights["Cybersecurity Analyst"]
    return (f"penetration testing={w['penetration testing']:.3f}, teamwork={w['teamwork']:.3f}",
            w["penetration testing"] > w["teamwork"])


def t_missing_excludes_matched():
    s, u, r = analyze(["python", "sql", "git"], "")
    ok = all(not ({m for m, _ in x["missing"]} & set(s)) for x in r)
    return "missing lists contain no selected skill", ok


def t_missing_order():
    s, u, r = analyze(["python", "sql"], "")
    ok = all([w for _, w in x["missing"]] == sorted([w for _, w in x["missing"]], reverse=True)
             for x in r)
    return "missing weights are non-increasing in every returned role", ok


def t_same_input_same_output():
    a = analyze(["python", "git"], "")[2]
    b = analyze(["python", "git"], "")[2]
    return "two runs compared", a == b


def t_data_integrity():
    df = pd.read_csv(ROOT / "data" / "role_profiles.csv")
    sizes = df.groupby("role").size()
    ok = (len(sizes) == 8 and sizes.between(25, 40).all()
          and set(df["skill"]) <= set(SKILLS))
    return f"roles={len(sizes)}, sizes={sizes.min()}-{sizes.max()}", ok


def t_zero_score_hidden():
    # html, css and react appear in only 2 role profiles, so the third slot
    # would be a role that shares no skill with the student.
    s, u, r = analyze(["html", "css", "react"], "")
    ok = 0 < len(r) < 3 and all(x["score"] > 0 for x in r)
    return f"{[(x['role'], x['score']) for x in r]}", ok


CASES = [
    ("T01", "empty", "empty string, nothing selected", "no skills, no results, no crash", t_empty),
    ("T02", "empty", "nothing selected, spaces typed", "no skills, no results", t_none_selected),
    ("T03", "invalid", "None for both inputs", "treated as empty, no crash", t_none_type),
    ("T04", "normal", "one skill: python", "3 roles returned, scores between 0 and 1", t_one_skill),
    ("T05", "unexpected", "all skills selected", "3 roles returned, scores between 0 and 1", t_all_skills),
    ("T06", "unexpected", "typed: pythno, javascrpit, postgre sql", "python and javascript recognized", t_misspelled),
    ("T07", "normal", "typed: py", "python", t_synonym_py),
    ("T08", "normal", "typed: ms sql, node, oop", "microsoft sql server, node.js, object-oriented programming", t_synonym_multi),
    ("T09", "unexpected", "python selected twice, typed Python, py, PYTHON", "python once", t_duplicates),
    ("T10", "invalid", "typed: @@@, ###, !!!, $$$", "no skills, no results", t_special_only),
    ("T11", "invalid", "typed: PYTHON!!! ; <script>alert(1)</script>", "python only", t_special_mixed),
    ("T12", "normal", "typed with mixed case and spaces", "python, sql", t_case_space),
    ("T13", "invalid", "typed: quantum basket weaving", "not recognized, no results", t_unknown_skill),
    ("T14", "unexpected", "teamwork, communication, problem solving", "3 roles, top score below 0.5", t_generic_skills),
    ("T15", "unexpected", "typed text of about 16,000 characters", "python once, no crash", t_long_input),
    ("T16", "normal", "penetration testing, siem, incident response", "top role Cybersecurity Analyst", t_security_profile),
    ("T17", "normal", "html, css, react, bootstrap, responsive design", "top role Web Developer", t_web_profile),
    ("T18", "normal", "vlan, routing, switching, cisco ios, subnetting", "top role Network Administrator", t_network_profile),
    ("T19", "normal", "TF-IDF weights in the Cybersecurity Analyst vector", "penetration testing weighs more than teamwork", t_idf_weight),
    ("T20", "normal", "python, sql, git", "no selected skill in any missing list", t_missing_excludes_matched),
    ("T21", "normal", "python, sql", "missing skills ordered by weight, heaviest first", t_missing_order),
    ("T22", "normal", "same input twice", "identical output", t_same_input_same_output),
    ("T23", "normal", "role_profiles.csv", "8 roles, 25 to 40 skills each, all in skills.csv", t_data_integrity),
    ("T24", "unexpected", "html, css, react", "fewer than 3 roles, no role with a score of 0", t_zero_score_hidden),
]


def run_all():
    rows = []
    for cid, kind, inp, expected, fn in CASES:
        try:
            actual, ok = fn()
        except Exception as exc:  # a crash is a failed test, not a stopped run
            actual, ok = f"{type(exc).__name__}: {exc}", False
        rows.append({"id": cid, "type": kind, "input": inp, "expected": expected,
                     "actual": actual, "result": "pass" if ok else "fail"})
    return rows


def test_all_cases():
    failed = [r for r in run_all() if r["result"] != "pass"]
    assert not failed, failed


if __name__ == "__main__":
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    rows = run_all()
    with open(out / "test_cases.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['id']} {r['result'].upper():4} {r['input']} -> {r['actual'][:90]}")
    passed = sum(r["result"] == "pass" for r in rows)
    print(f"\n{passed} of {len(rows)} test cases passed.")
