"""Evaluation module.

Measures top-3 accuracy on labeled student profiles, compares it with two
baselines, lists every wrong result and builds a role confusion table.

Run from the project folder:
    python -m src.evaluate
    python -m src.evaluate --profiles data/student_profiles.csv
"""
import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd

from src import skill_input
from src.matcher import RoleMatcher

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
MOCK_BANNER = "MOCK DATA: manually created profiles, not collected from students"

# Pairs that share many skills. Checked first when explaining an error.
OVERLAP_PAIRS = [
    {"Software Developer", "Web Developer"},
    {"Network Administrator", "IT Support Specialist"},
]


def default_profiles_path():
    """Use the collected-student file when it exists, otherwise the mock file."""
    real = DATA_DIR / "student_profiles.csv"
    return real if real.exists() else DATA_DIR / "student_profiles_MOCK.csv"


def is_mock(path, df):
    if "MOCK" in Path(path).name.upper():
        return True
    return "data_type" in df.columns and (df["data_type"].astype(str).str.lower() == "mock").any()


def likely_cause(matcher, true_role, top3_roles, n_skills):
    """Return a short, checkable reason for one wrong result."""
    top1 = top3_roles[0] if top3_roles else None
    if not top3_roles:
        return "No selected skill appears in any role profile."
    if n_skills < 5:
        return f"Only {n_skills} skills were selected, too few to separate roles."
    pair = {true_role, top1}
    shared = set(matcher.role_skills[true_role]) & set(matcher.role_skills[top1])
    if pair in OVERLAP_PAIRS:
        return (f"{true_role} and {top1} are a known overlap pair "
                f"({len(shared)} shared role skills).")
    return (f"Selected skills match {top1} more closely than {true_role} "
            f"({len(shared)} shared role skills between the two).")


def evaluate(profiles_path=None, matcher=None, skills=None, synonyms=None):
    profiles_path = Path(profiles_path or default_profiles_path())
    df = pd.read_csv(profiles_path)
    matcher = matcher or RoleMatcher()
    skills = skills or skill_input.load_skills()
    synonyms = synonyms or skill_input.load_synonyms()
    mock = is_mock(profiles_path, df)

    rows, errors = [], []
    confusion = Counter()
    for _, rec in df.iterrows():
        raw = str(rec["skills"]).replace(";", ",")
        student, _ = skill_input.clean_entries(raw, skills, synonyms)
        recs = matcher.recommend(student, top_n=3)
        top3 = [r["role"] for r in recs]
        true_role = str(rec["true_role"]).strip()
        hit = true_role in top3
        top1 = top3[0] if top3 else "(no result)"
        confusion[(true_role, top1)] += 1
        rows.append(hit)
        if not hit or top1 != true_role:
            errors.append({
                "profile_id": rec["profile_id"],
                "error_type": "top-3 miss" if not hit else "top-1 miss only (true role is in top 3)",
                "true_role": true_role,
                "recommended_top3": " | ".join(top3) if top3 else "(no result)",
                "n_skills": len(student),
                "likely_cause": likely_cause(matcher, true_role, top3, len(student))
                if true_role in matcher.role_skills else "True role is not one of the 8 roles.",
            })

    total = len(df)
    correct = sum(rows)
    n_roles = len(matcher.roles)
    top1_correct = sum(n for (t, p), n in confusion.items() if t == p)

    role_counts = Counter(df["true_role"].str.strip())
    common3 = [r for r, _ in sorted(role_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
    common_hits = sum(1 for r in df["true_role"].str.strip() if r in common3)

    result = {
        "banner": MOCK_BANNER if mock else "Profiles collected from students",
        "profiles_file": profiles_path.name,
        "total_profiles": total,
        "top3_correct": correct,
        "top3_accuracy_percent": round(100 * correct / total, 1) if total else None,
        "top1_correct": top1_correct,
        "top1_accuracy_percent": round(100 * top1_correct / total, 1) if total else None,
        "random_baseline_top3_percent": round(100 * 3 / n_roles, 1),
        "most_common_roles": common3,
        "most_common_baseline_top3_percent": round(100 * common_hits / total, 1) if total else None,
        "target_top3_percent": 80,
        "met_target": bool(total and 100 * correct / total >= 80),
        "points_per_wrong_result": round(100 / total, 1) if total else None,
        "note": (f"One wrong result moves top-3 accuracy by about {round(100 / total, 1)} "
                 f"points on {total} profiles.") if total else "",
    }
    return result, pd.DataFrame(errors), confusion, matcher.roles


def write_results(result, errors, confusion, roles, out_dir=None):
    out = Path(out_dir or RESULTS_DIR)
    out.mkdir(parents=True, exist_ok=True)
    mock = result["banner"] == MOCK_BANNER

    with open(out / "accuracy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    cm = pd.DataFrame(0, index=roles, columns=roles + ["(no result)"])
    for (t, p), n in confusion.items():
        if t in cm.index and p in cm.columns:
            cm.loc[t, p] = n
    cm.index.name = "true_role"

    for name, frame, index in (("errors.csv", errors, False), ("confusion.csv", cm, True)):
        with open(out / name, "w", encoding="utf-8", newline="") as f:
            if mock:
                f.write(f"# {MOCK_BANNER}\n")
            frame.to_csv(f, index=index)


def print_report(result, errors):
    if result["banner"] == MOCK_BANNER:
        print(MOCK_BANNER)
        print("-" * len(MOCK_BANNER))
    t = result["total_profiles"]
    print(f"Profiles file: {result['profiles_file']} ({t} profiles)")
    print(f"Top-3 accuracy: {result['top3_accuracy_percent']}% "
          f"({result['top3_correct']} of {t} profiles have the true role in the top 3)")
    print(f"Top-1 accuracy: {result['top1_accuracy_percent']}% "
          f"({result['top1_correct']} of {t} profiles have the true role ranked first)")
    print(f"Random baseline (top-3 accuracy): {result['random_baseline_top3_percent']}%")
    print(f"Most-common-roles baseline (top-3 accuracy): "
          f"{result['most_common_baseline_top3_percent']}% "
          f"(roles: {', '.join(result['most_common_roles'])})")
    print(f"Target top-3 accuracy: {result['target_top3_percent']}%. "
          f"Met: {'yes' if result['met_target'] else 'no'}")
    print(result["note"])
    if len(errors):
        print("\nWrong results:")
        print(errors.to_string(index=False))


def main():
    ap = argparse.ArgumentParser(description="Top-3 accuracy of the Matching module.")
    ap.add_argument("--profiles", default=None, help="CSV of labeled student profiles")
    ap.add_argument("--out", default=None, help="results folder")
    args = ap.parse_args()
    result, errors, confusion, roles = evaluate(args.profiles)
    write_results(result, errors, confusion, roles, args.out)
    print_report(result, errors)


if __name__ == "__main__":
    main()
