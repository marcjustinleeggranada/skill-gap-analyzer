# Decisions

Log of project decisions. Newest first. Add a dated entry for every decision, then commit and push it.

## 2026-11-01 (strict sourcing, mock test set)

- Sourcing standard (owner delegated the choice): a source backs a skill only if the page names the skill or a standard synonym. A tool counts only when the skill is that tool. Skills implied by related tasks, example tools of another skill or category headings do not count. Closed, expired or removed pages do not count. 2 or more live sources = backed, 1 = `SINGLE SOURCE <ID>`, 0 = `UNVERIFIED`.
- Audited all 34 sources against that rule. CA-2 (page gone) and NA-2 (closed) were removed. Added 22 live sources (34 - 2 removed + 22 = 54) (CA-5 to CA-9, NA-6 to NA-9, QA-5 to QA-7, DBA-5 to DBA-7, IT-6 to IT-8, SD-5, WD-5, WD-6, DA-5). Now 54 sources.
- Result: 128 rows backed, 62 single source, 50 unverified (was 107 / 61 / 72 under the looser rule). Sourcing stopped here. No skill was dropped or renamed.
- Postings expire and the workspace cannot reach archive sites. The team must save archive copies.
- Test set (owner decision): real student profiles will not be collected. `data/student_profiles_MOCK.csv` has 32 manually created profiles (4 per role), written before the first run and not tuned. The instructor guidelines allow manually created examples. Results carry the line "MOCK DATA: manually created profiles, not collected from students".
- First run: top-3 100% (32 of 32), top-1 96.9%. Reported as optimistic because the profiles are clean and typical. Not tuned to reach 80%.
- The paper chat must update Chapter 3, the ethics section and the weekly report: no student data was collected, the test set is manually created.
- Replaced `student_profiles_SAMPLE.csv` and the `SAMPLE` banner with the mock file and banner. Added test T28 (mock data integrity). 28 test cases.
- The history rewrite for the wrong email was done by the owner's other session. This clone was reset to it. All 9 commits now carry the correct email.

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

## 2026-11-01 (link check)

- Opened all 34 URLs in `sources/sources.csv`. 32 load with their posting or reference content. Results are in `sources/link_check.csv`.
- NA-2 loads but shows "Job closed". CA-2 no longer exists. Both are kept in place until the owner decides.
- No archived copies were saved. The workspace cannot reach archive sites, so web archive links and PDFs of the postings are still open. The owner can save them from a browser, or approve a fetch of the archive service.
- `data/role_profiles.csv` was not changed.

## 2026-11-01 (paper and weekly report)

- Paper Chapter 3, the ethics section and the weekly report now say plainly that no student data was collected and that the test set is 32 manually created profiles, 4 per role.
- The paper and the weekly report call the 100% top-3 result (32 of 32) optimistic, because the profiles are clean and typical. They say it shows the method works and does not predict real students.
- Objectives, Scope, Limitations, Significance and the testing plan changed from about 30 volunteer profiles to the 32 manual ones. One wrong result now moves accuracy about 3.1 points.
- Chapter 4 holds the first-run numbers from Build_Status.md. Screenshots and the error list are added after final testing.
- The paper describes the system with the real numbers: 28 to 32 skills per role and a list of 112 skills. The original targets (25 to 40 skills, about 100 listed) stay as planned figures in parentheses.

## 2026-11-01 (source counts in the paper)

- Chapter 3 now gives the label counts: 128 backed (53.3%), 62 single source (25.8%), 50 unverified (20.8%), out of 240 rows.
- `sources/sources.csv` has 54 sources: 41 job postings and 13 occupation or reference pages. Every one is cited by at least one row. The earlier figure of 52 sources, and the line "Added 18 live sources", do not match the file (the IDs added are 22, which gives 54). The coding side corrects Build_Status.md and the earlier entry.

## 2026-11-01 (source count fixed in status files)

- Corrected the earlier count: 22 sources were added, not 18, so the total is 54, not 52. Fixed in `Build_Status.md` and the strict-sourcing entry above. README and `sources_apa.md` never gave the total.

## 2026-11-01 (paper limitations and sizes)

- Chapter 3 lists the skills per role (32, 32, 31, 30, 30, 29, 28, 28 for 240 rows) and says unverified rows stay in the profiles and are used by the matcher.
- The paper Limitations now state that postings expire with no archived copies, that skills are matched by name only with no weight for skill level, that two role pairs overlap heavily (Software Developer and Web Developer; Network Administrator and IT Support Specialist), and that the instructor has not confirmed the eight roles.
- Chapter 4 names the one top-1 miss as profile M04.

## 2026-11-01 (progress report and paper chapters 4 and 5)

- Instructor left the choice of the eight roles to the group. The paper and the report no longer list the roles as unconfirmed; the paper keeps one limitation that no outside check of the role list exists.
- Report roles: Granada project lead and coordination; Tabares data and sourcing; Morales matching and TF-IDF code; Berona interface and Streamlit screen; Arimatea and Paredes testing and evaluation; Delos Santos documentation and paper.
- Report dates are planned weekly periods: Week 1 October 12 to 18, Week 2 October 19 to 25, Week 3 October 26 to November 1, Week 4 November 2 to 8, Week 5 November 9 to 15, Week 6 November 16 to 22. Weeks 4 and 5 work was finished early, on November 1.
- Report overall completion is 70%, status on track. Weeks 3 to 5 are filled; Week 6 is blank.
- Paper Chapter 4 now has test cases, accuracy by role, error analysis (profile M04) and screen sections. Chapter 5 has the conclusion against the four objectives and the recommendations.
- Chapter 4 points to the screenshots and test case file in the project files; the group still picks which screenshots go in the final document.
- Ali et al. (2022) reference now has volume 41, issue 1 from the journal site. Page numbers are not listed there. The JITK journal name was checked against the journal page.
- The test set stays manual. No real student profiles will be collected.
