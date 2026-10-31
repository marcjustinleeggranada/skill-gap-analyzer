# Build Status: Skill Gap Analyzer

Date: 2026-11-01. Scope built: everything in Proposal1_Build_Spec.md (option 3), with sample data only.

## What works

- The Skill Input module cleans typed text, applies 39 synonyms, fixes close misspellings and keeps only terms in `skills.csv` (112 skills).
- The Matching module fits a scikit-learn `TfidfVectorizer` (TF-IDF: Term Frequency-Inverse Document Frequency) on 8 role documents and ranks roles by cosine similarity. It returns the top 3 roles. Roles with a score of 0 share no skill with the student and are left out, so fewer than 3 roles can come back.
- The Skill Gap module lists matched and missing skills per role, ordered by TF-IDF weight.
- The Streamlit screen has a multi-select list, a box for typed skills, an Analyze button, the top 3 roles with scores (or "Closest roles" and a note when fewer than 3 roles share a skill with the input), matched skills, missing skills, a message for empty input and a line saying the output is guidance, not a hiring decision. It stores nothing.
- `src/evaluate.py` computes top-3 accuracy, top-1 accuracy, the random baseline, the most-common-roles baseline, the error list and a role confusion table.
- 24 of 24 test cases pass (`python tests/test_cases.py`).
- The screen was opened in a browser on 2026-11-01: it loads, shows the empty-input warning, and returns 3 roles for the demo input. Details and screenshots are in Build_Report.md.

## How to run

```
pip install -r requirements.txt
streamlit run app.py
python -m src.evaluate
python tests/test_cases.py
```

Details are in README.md.

## Real numbers

None yet. Real student profiles do not exist, so there is no project accuracy.

Pipeline check on `student_profiles_SAMPLE.csv` (SAMPLE DATA, NOT A PROJECT RESULT, do not cite):

- Top-3 accuracy: 30 of 30 profiles (100%). Top-1 accuracy: 26 of 30 (86.7%).
- Random baseline: 37.5%. Most-common-roles baseline: 40.0%.
- The 4 top-1 misses are the profiles written on purpose to overlap: Software Developer vs Web Developer (2) and Network Administrator vs IT Support Specialist (2).
- Why 100% means little: 26 of the 30 sample profiles were drawn at random from each role's own skill list, so they match their role by construction. Real profiles will score lower.

Test-case result (real, this is a code check, not an accuracy figure): 24 of 24 passed.

One wrong result moves top-3 accuracy by about 3.3 points on 30 profiles.

## Files produced

- `app.py`, `src/skill_input.py`, `src/matcher.py`, `src/skill_gap.py`, `src/evaluate.py`
- `tests/test_cases.py`
- `data/skills.csv`, `data/synonyms.csv`, `data/role_profiles.csv`, `data/student_profiles_SAMPLE.csv`
- `results/accuracy.json`, `results/errors.csv`, `results/confusion.csv`, `results/test_cases.csv` (the first three are built from sample data and carry the banner)
- `requirements.txt` (scikit-learn 1.9.1, pandas 3.0.5, streamlit 1.66.1), `README.md`

## Changes from the spec

- `errors.csv` has an extra `error_type` column and also lists top-1 misses where the true role is still in the top 3. Reason: the sample data has no top-3 misses, so this keeps the error code exercised. Top-3 misses are tagged "top-3 miss".
- Added `results/confusion.csv` (true role against role ranked first).
- Roles with a score of 0 are not shown. Before 2026-11-01 the screen could list such a role in third place with no matched skills.

## Assumptions

- Web search was not used. Role skills, the skill list and the synonyms come from general knowledge, so every `role_profiles.csv` row is `UNVERIFIED`. No source was invented.
- Role sizes are 28 to 32 skills. The skill list has 112 skills (spec says about 100).
- Typed words of 5 or more letters are matched to the closest skill when the spelling similarity is at least 0.8 (Python `difflib`). Shorter words must match exactly or through the synonym table.
- The `k8s` synonym from the decisions file is left out because no Kubernetes skill is in the list.
- Selected list items also pass through the cleaning step.
- The sample banner is not shown on the screen because the screen reports no accuracy. It appears in the console and in the saved result files.
- Skills with no place in any role profile are ignored by the score. If none of a student's skills are in any role profile, the screen says no role can be scored.
- Profile skills in CSV files are separated by semicolons.

## Still UNVERIFIED

- All 240 rows in `role_profiles.csv` (8 roles, 240 role-skill pairs).
- The synonym table and the skill categories.

## Open items for the team

- Check each role skill against a real posting or curriculum and write the reference in the `source` column.
- Confirm the 8 roles with the instructor.
- Write the consent text and collect about 30 real student profiles (skills selected plus target role; no names, contact details or student numbers). Save as `data/student_profiles.csv`, then run `python -m src.evaluate`.
- Pick the screenshots for Chapter 4 from `results/screenshots/`.
- Record who covers which part in the progress report.
