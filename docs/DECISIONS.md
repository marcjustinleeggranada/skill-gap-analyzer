# Decisions

Log of project decisions. Newest first. Add a dated entry for every decision, then commit and push it.

## 2026-11-01 (screenshots)

- Retake screenshots 01 to 06 so they show the new draft notice.

## 2026-11-01 (zero-score roles)

- Hide roles with a score of 0. They share no skill with the student, so showing them as a recommendation misleads.
- Show the heading "Closest roles" and a note when fewer than 3 roles remain.
- Add test T24 for this case. The test count is now 24.

## 2026-11-01 (build check)

- Verified the build on a fresh clone: 23 of 23 test cases pass, and the sample evaluation output matches Build_Status.md.
- Recorded the results in Build_Report.md and saved 5 screen screenshots in `results/screenshots/`.
- Left roles that score 0.00 visible in the top 3 for now. The check allows fixes only for failures. The team decides whether to hide them.
- Left `data/role_profiles.csv` unchanged while its sources are collected.

## 2026-11-01

- Sourcing: role skills were checked against 34 opened pages (job postings, Occupational Outlook Handbook and O*NET OnLine summaries, one CompTIA exam objectives document). Output is in `sources/`.
- Sourcing rule applied: 2 or more sources for a role back a skill; 1 source is marked SINGLE SOURCE; skills with no source stay UNVERIFIED. A skill in a posting's skill tags counts as named.
- Sourcing result: 107 skills backed, 61 single source, 72 unverified, out of 240. `data/role_profiles.csv` is unchanged; the coding side decides when to adopt the sourced file.
- Suggested additions are listed in `sources/sources_apa.md` and were not added to the CSV.
- Adopted: `data/role_profiles.csv` now carries the sourced `source` column. Roles and skills are unchanged. Source IDs refer to `sources/sources.csv`.
- The 72 rows still marked `UNVERIFIED` stay so, and the app keeps its unverified notice. The README and Build_Status.md lines saying all 240 rows are unverified are out of date; the coding side updates them.
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

## 2026-11-01 (source check)

- Spot-checked 3 sources by opening them. SD-1 supports all 10 attributed skills. SD-4 supports its skills, loosely for unit testing, ci/cd, debugging and technical documentation. CA-2 returned "Job Not Found".
- 14 Cybersecurity Analyst rows cite CA-2. 4 would have no source without it and 6 would drop to one source. The team decides whether to replace it.
- Updated README.md and Build_Status.md for the sourced role profiles.
- Removed network addresses from Build_Report.md.

## 2026-11-01 (git guard and input fixes)

- Commit identity: Marc Justin Lee G. Granada, granadamarc96@gmail.com. No other email is correct. Rules and the push check are in `docs/GIT_RULES.md` and `.githooks/pre-push`.
- Two earlier commits still carry granadam96@gmail.com. Correcting them needs a history rewrite and a force push, which only the owner approves. Steps are in `docs/GIT_RULES.md`.
- Never rewrite history or force-push without the owner's approval.
- Strip accents from Latin letters in typed skills. List entries in other scripts as not recognized. Symbols and emoji alone stay ignored.
- Add `requirements-dev.txt` for pytest and a Windows `py` note in the README.
- Test count is now 27.
- Reword the on-screen draft notice, because 107 of 240 role skills now have 2 or more sources. Screenshots 01 to 06 show the old wording and need retaking.
- The repository is public. The earlier build report put a network address into commit history. Visibility and history cleanup are the owner's decision.
