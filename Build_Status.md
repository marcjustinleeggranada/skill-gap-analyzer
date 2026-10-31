# Build Status: Skill Gap Analyzer

Date: 2026-11-01. Scope built: everything in Proposal1_Build_Spec.md (option 3), with a manually created mock test set.

## What works

- The Skill Input module cleans typed text, applies 39 synonyms, fixes close misspellings and keeps only terms in `skills.csv` (112 skills).
- The Matching module fits a scikit-learn `TfidfVectorizer` (TF-IDF: Term Frequency-Inverse Document Frequency) on 8 role documents and ranks roles by cosine similarity. It returns the top 3 roles. Roles with a score of 0 share no skill with the student and are left out, so fewer than 3 roles can come back.
- The Skill Gap module lists matched and missing skills per role, ordered by TF-IDF weight.
- The Streamlit screen has a multi-select list, a box for typed skills, an Analyze button, the top 3 roles with scores (or "Closest roles" and a note when fewer than 3 roles share a skill with the input), matched skills, missing skills, a message for empty input and a line saying the output is guidance, not a hiring decision. It stores nothing.
- `src/evaluate.py` computes top-3 accuracy, top-1 accuracy, the random baseline, the most-common-roles baseline, the error list and a role confusion table.
- 28 of 28 test cases pass (`python tests/test_cases.py`).
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

No profiles were collected from students. The test set is `data/student_profiles_MOCK.csv`: 32 manually created profiles, 4 per role, written by hand as typical entry-level skill sets before the first run and not changed afterwards (disclose this as a manually created test set; the instructor guidelines allow manually created examples).

- Top-3 accuracy: 32 of 32 profiles (100%). Target is 80%. Top-1 accuracy: 31 of 32 (96.9%).
- Random baseline: 37.5%. Most-common-roles baseline: 37.5% (all roles are equally common, so the baseline ties with random).
- The one top-1 miss is M04, a Software Developer profile (python, javascript, git, ci/cd, docker, unit testing, sql, technical documentation, agile) that ranked Quality Assurance Tester first. The true role is second.
- How to read 100%: the profiles are clean, typical sets written from the same kind of role knowledge as the role profiles, with no deliberately confusing cases, so the number is optimistic. It shows the method and code work. It does not predict how real students will score. Say this in the paper.

Test-case result (code check, not an accuracy figure): 28 of 28 passed.

One wrong result moves top-3 accuracy by about 3.1 points on 32 profiles.

## Files produced

- `app.py`, `src/skill_input.py`, `src/matcher.py`, `src/skill_gap.py`, `src/evaluate.py`
- `tests/test_cases.py`
- `data/skills.csv`, `data/synonyms.csv`, `data/role_profiles.csv`, `data/student_profiles_MOCK.csv`
- `results/accuracy.json`, `results/errors.csv`, `results/confusion.csv`, `results/test_cases.csv` (the first three are built from mock data and carry the banner)
- `requirements.txt` (scikit-learn 1.9.1, pandas 3.0.5, streamlit 1.66.1), `README.md`

## Changes from the spec

- `errors.csv` has an extra `error_type` column and also lists top-1 misses where the true role is still in the top 3. Reason: the mock data has no top-3 misses, so this keeps the error code exercised. Top-3 misses are tagged "top-3 miss".
- Added `results/confusion.csv` (true role against role ranked first).
- The Skill Input module now removes accents from Latin letters and lists entries in other scripts as not recognized (tests T25 to T27). Before, accented letters turned into spaces and other scripts were dropped without a message.
- Added `requirements-dev.txt` (pytest) and a Windows note for the `py` launcher in README.md.
- Added `docs/GIT_RULES.md` and `.githooks/pre-push`. Turn the hook on with `git config core.hooksPath .githooks`.
- Roles with a score of 0 are not shown. Before 2026-11-01 the screen could list such a role in third place with no matched skills.

## Assumptions

- Role skills were checked against 52 opened pages (see `sources/`). A page backs a skill only if it names the skill or a standard synonym; implied skills, example tools of another skill, closed pages and expired pages do not count. The skill list and synonyms come from general knowledge. No source was invented. Rows no page names keep `UNVERIFIED`.
- Role sizes are 28 to 32 skills. The skill list has 112 skills (spec says about 100).
- Typed words of 5 or more letters are matched to the closest skill when the spelling similarity is at least 0.8 (Python `difflib`). Shorter words must match exactly or through the synonym table.
- The `k8s` synonym from the decisions file is left out because no Kubernetes skill is in the list.
- Selected list items also pass through the cleaning step.
- The mock banner is not shown on the screen because the screen reports no accuracy. It appears in the console and in the saved result files.
- Skills with no place in any role profile are ignored by the score. If none of a student's skills are in any role profile, the screen says no role can be scored.
- Profile skills in CSV files are separated by semicolons.

## Still UNVERIFIED

- 50 of 240 rows in `role_profiles.csv` have no source. 62 more rows rest on a single source. 128 are backed by 2 or more live sources.
- CA-2 (page gone) and NA-2 (closed) were removed and replaced with live sources (CA-5, CA-6, NA-6 to NA-9). Postings expire, so no source is archived yet.
- The strict counting rule dropped many earlier "backed" rows. For example, SD-4 (O*NET OnLine) no longer counts for unit testing, ci/cd, debugging and technical documentation because it only implies them.
- The synonym table and the skill categories.

## Open items for the team

- Save an archive copy (PDF or web archive link) of every posting in `sources/sources.csv`; record it in `sources/link_check.csv`.
- Check the single-source and unverified rows against more postings or the curriculum, or accept them as drafts.
- Confirm the 8 roles with the instructor.
- The test set is mock (manually created). The paper chat must update Chapter 3, the ethics section and the weekly report to say so. If the team later collects real profiles, save them as `data/student_profiles.csv` and run `python -m src.evaluate`.
- Pick the screenshots for Chapter 4 from `results/screenshots/`.
- Record who covers which part in the progress report.
