# Decisions

Log of project decisions. Newest first. Add a dated entry for every decision, then commit and push it.

## 2026-11-01 (build check)

- Verified the build on a fresh clone: 23 of 23 test cases pass, and the sample evaluation output matches Build_Status.md.
- Recorded the results in Build_Report.md and saved 5 screen screenshots in `results/screenshots/`.
- Left roles that score 0.00 visible in the top 3 for now. The check allows fixes only for failures. The team decides whether to hide them.
- Left `data/role_profiles.csv` unchanged while its sources are collected.

## 2026-11-01

- Input: the student selects skills from a list of 112 skills and can type extras. There is no resume input.
- Method: TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity on 8 role documents. No model training.
- Roles: the 8 roles are final for now. They live in `data/role_profiles.csv` so the instructor can change them.
- Sources: role skills stay `UNVERIFIED` until backed by real postings or curricula. No invented sources, URLs or numbers.
- Sourcing rule: at least 3 sources per role. A skill counts as backed when at least 2 sources for that role name it.
- Sample data: `data/student_profiles_SAMPLE.csv` is made up. Results from it carry the line "SAMPLE DATA, NOT A PROJECT RESULT" and are never cited as the project's accuracy.
- Real data: collect about 30 profiles with written consent, no names, contact details or student numbers. Save as `data/student_profiles.csv`.
- Evaluation: top-3 accuracy against two baselines (random: 37.5%, most-common-roles). Target: 80%. One wrong result moves accuracy about 3.3 points on 30 profiles.
- Typed words of 5 or more letters are matched to the closest skill at a spelling similarity of 0.8 or higher.
- Git workflow: run `git pull` before starting any work. Push updates and decisions after each change.
- Commits use the author's name only: Marc Justin Lee G. Granada.
