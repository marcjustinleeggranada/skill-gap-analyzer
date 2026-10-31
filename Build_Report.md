# Build Report: Skill Gap Analyzer

Date: 2026-11-01. Machine: Windows 11 Home Single Language. Code: a fresh clone of `main` at commit `3b5d603`. Every result below comes from a real run on this machine. No output was edited by hand.

## Environment

- `python --version` failed. Exact message: `Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.` (exit code 9009). On this machine the `python` command is the Windows Store placeholder, not a real install.
- The Python launcher works: `py --version` printed `Python 3.14.6`.
- A virtual environment was created with `py -3.14 -m venv .venv`. Every command below ran with `.venv\Scripts\python.exe`. The `.venv/` folder is already in `.gitignore`.
- `pip install -r requirements.txt`: succeeded with exit code 0. No install errors. The only extra text was a notice that a newer pip is available.

| Library | Installed version |
|---|---|
| Python | 3.14.6 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.5 |
| streamlit | 1.66.1 |
| numpy (installed as a dependency) | 2.5.4 |
| scipy (installed as a dependency) | 1.18.1 |

## Test results

First run, on the code as cloned: 23 of 23 test cases passed. Exit code 0. No failure text.

Second run, after the change in "Files changed" added test T24: 24 of 24 test cases passed. Exit code 0. No failure text. T01 to T23 printed the same lines as below, plus:

```
T24 PASS html, css, react -> [('Web Developer', 0.3933), ('Quality Assurance Tester', 0.1075)]

24 of 24 test cases passed.
```

Full console output of the first run of `python tests/test_cases.py`. Lines T04, T05 and T14 are cut short by the test script itself, not by this report. The exclamation points in T10 and T11 are part of those test inputs and are kept as printed.

```
T01 PASS empty string, nothing selected -> skills=[], results=[]
T02 PASS nothing selected, spaces typed -> skills=[], results=[]
T03 PASS None for both inputs -> skills=[], results=[]
T04 PASS one skill: python -> [('Database Administrator', 0.1268), ('Quality Assurance Tester', 0.1257), ('Software Deve
T05 PASS all skills selected -> 112 skills, top3=[('Data Analyst', 0.4725), ('Network Administrator', 0.4663), ('Web Devel
T06 PASS typed: pythno, javascrpit, postgre sql -> skills=['python', 'javascript', 'postgresql'], unrecognized=[]
T07 PASS typed: py -> skills=['python']
T08 PASS typed: ms sql, node, oop -> skills=['microsoft sql server', 'node.js', 'object-oriented programming']
T09 PASS python selected twice, typed Python, py, PYTHON -> skills=['python']
T10 PASS typed: @@@, ###, !!!, $$$ -> skills=[], results=[]
T11 PASS typed: PYTHON!!! ; <script>alert(1)</script> -> skills=['python'], unrecognized=['script alert 1 /script']
T12 PASS typed with mixed case and spaces -> skills=['python', 'sql']
T13 PASS typed: quantum basket weaving -> skills=[], unrecognized=['quantum basket weaving']
T14 PASS teamwork, communication, problem solving -> top3=[('IT Support Specialist', 0.1756), ('Database Administrator', 0.1755), ('Quality Ass
T15 PASS typed text of about 16,000 characters -> skills=['python']
T16 PASS penetration testing, siem, incident response -> top1=Cybersecurity Analyst
T17 PASS html, css, react, bootstrap, responsive design -> top1=Web Developer
T18 PASS vlan, routing, switching, cisco ios, subnetting -> top1=Network Administrator
T19 PASS TF-IDF weights in the Cybersecurity Analyst vector -> penetration testing=0.239, teamwork=0.096
T20 PASS python, sql, git -> missing lists contain no selected skill
T21 PASS python, sql -> missing weights are non-increasing in every returned role
T22 PASS same input twice -> two runs compared
T23 PASS role_profiles.csv -> roles=8, sizes=28-32

23 of 23 test cases passed.
```

## Evaluation output

`python -m src.evaluate` finished with exit code 0. Full console output:

```
SAMPLE DATA, NOT A PROJECT RESULT
---------------------------------
Profiles file: student_profiles_SAMPLE.csv (30 profiles)
Top-3 accuracy: 100.0% (30 of 30 profiles have the true role in the top 3)
Top-1 accuracy: 86.7% (26 of 30 profiles have the true role ranked first)
Random baseline (top-3 accuracy): 37.5%
Most-common-roles baseline (top-3 accuracy): 40.0% (roles: Data Analyst, IT Support Specialist, Network Administrator)
Target top-3 accuracy: 80%. Met: yes
One wrong result moves top-3 accuracy by about 3.3 points on 30 profiles.

Wrong results:
profile_id                              error_type             true_role                                                      recommended_top3  n_skills                                                                                      likely_cause
      S005 top-1 miss only (true role is in top 3) IT Support Specialist Network Administrator | IT Support Specialist | Cybersecurity Analyst         8 IT Support Specialist and Network Administrator are a known overlap pair (21 shared role skills).
      S012 top-1 miss only (true role is in top 3)    Software Developer         Web Developer | Quality Assurance Tester | Software Developer         8            Software Developer and Web Developer are a known overlap pair (19 shared role skills).
      S013 top-1 miss only (true role is in top 3) Network Administrator IT Support Specialist | Network Administrator | Cybersecurity Analyst         8 Network Administrator and IT Support Specialist are a known overlap pair (21 shared role skills).
      S028 top-1 miss only (true role is in top 3)         Web Developer         Software Developer | Quality Assurance Tester | Web Developer         8            Web Developer and Software Developer are a known overlap pair (19 shared role skills).
```

What the numbers measure:

- Top-3 accuracy: the share of profiles whose true role is among the 3 roles ranked highest.
- Top-1 accuracy: the share of profiles whose true role is ranked first.
- Random baseline: the top-3 accuracy of picking 3 of the 8 roles at random (3 divided by 8).
- Most-common-roles baseline: the top-3 accuracy of always answering with the 3 roles that appear most often in the profiles file.

These numbers match Build_Status.md. The evaluation was run again after the change in "Files changed" and printed the same numbers and the same 4 wrong results. They come from the 30 made-up sample profiles and only show that the code runs. They are not the project's accuracy.

The test and evaluation scripts rewrote the files in `results/`. Their content is the same as the committed copies. Git records no change for them.

## Screen check

- Did it start: yes. Command: `streamlit run app.py --server.headless true --server.port 8502`, run with the virtual environment's Python. Port 8502 was used because 8501 had been used by an earlier check on this machine. Startup log:

```
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

2026-11-01 04:23:44.635 Uvicorn server started on :::8502

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8502
  Network URL: (address removed)
  External URL: (address removed)
```

- Opened in a browser: yes, at `http://localhost:8502`. The page showed the title, the description, the notice that the role profiles are drafts, the skills list, the typed box and the Analyze button.
- Empty input: pressing Analyze with nothing entered showed: "No skills were entered. Select at least one skill from the list or type a skill name, then press Analyze."
- Did Analyze work: yes. Input: `html`, `css`, `react` and `git` selected, `py, js` typed. Result on screen ("score" is the cosine similarity between the student's skills and the role, on a scale of 0 to 1):
  1. Web Developer, score 0.47. Matched skills: css, react, html, javascript, git, python.
  2. Quality Assurance Tester, score 0.23. Matched skills: html, javascript, git, python.
  3. Software Developer, score 0.14. Matched skills: javascript, git, python.
  Each role also listed its missing skills. `py` was read as python and `js` as javascript.
- Guidance line at the bottom: "This output is guidance for study planning. It is not a hiring decision."
- Note on entering skills: after each pick, the skills list closes and the page reloads. The list has to be opened again for the next skill.

Screenshot files in `results/screenshots/`:

| File | Shows |
|---|---|
| `01_demo_input.jpg` | html, css, react and git selected and `py, js` typed, before Analyze |
| `02_empty_input_message.jpg` | the empty-input message |
| `03_analyze_result_top.jpg` | the input and the start of the result after Analyze |
| `04_analyze_result_roles.jpg` | the top 3 roles with scores, matched skills and missing skills |
| `05_guidance_line.jpg` | the end of the result with the guidance line at the bottom |
| `06_zero_score_roles_hidden.jpg` | after the change: `html, css, react` typed, the heading "Closest roles", the note "Only 2 of the 8 roles share a skill with your input. Roles with a score of 0 are not shown.", and 2 roles |

Screenshots 01 to 05 were taken before the change. After the change, the demo input still returns Web Developer 0.47, Quality Assurance Tester 0.23 and Software Developer 0.14, so those screenshots still match the screen.

## Extra inputs tried

Each input was typed into the "Other skills" box with nothing selected, then Analyze was pressed. The inputs were run against `app.py` itself with Streamlit's built-in test harness (`streamlit.testing.v1.AppTest`), which runs the same script and the same button as the browser. No input raised an error.

| Input | Expected | Actual | Result |
|---|---|---|---|
| Very long text: `html, css, ` repeated 10,000 times plus `react` (110,005 characters) | No crash, no long wait; html, css and react recognized; Web Developer first | First run: no error. Analyze took 0.06 seconds. Matched css, react, html. 1. Web Developer 0.39, 2. Quality Assurance Tester 0.11, 3. Cybersecurity Analyst 0.00 with "Matched skills: none". After the change: only roles 1 and 2 shown, with the note "Only 2 of the 8 roles share a skill with your input. Roles with a score of 0 are not shown." | Pass (the 0.00 role is fixed, see Files changed) |
| Emoji: a snake emoji then `python`, a coffee emoji then `java`, a rocket emoji alone, `sql` then a heart emoji | Emoji removed; python, java and sql recognized | Matched java, sql, python. 1. Quality Assurance Tester 0.28, 2. Software Developer 0.28, 3. Database Administrator 0.13. The emoji were removed without a message | Pass |
| Mixed languages: `Python, base de datos, ` then "database" in Japanese, `programación, sql, ` then "web" in Russian | No crash; python and sql recognized; other entries not matched | Matched sql, python. 1. Database Administrator 0.19, 2. Quality Assurance Tester 0.19, 3. Software Developer 0.19. Caption: "Not recognized and left out: base de datos, programaci n". The Japanese and Russian entries were dropped without being listed | Pass (see problem 3) |
| Only spaces: 8 spaces | Empty-input message, no roles | "No skills were entered. Select at least one skill from the list or type a skill name, then press Analyze." No roles shown | Pass |
| Typos: `javascirpt, ptyhon, kubernets, sq, htlm` | javascript and python corrected; `sq` and `htlm` not corrected (under 5 letters, by design); `kubernets` not recognized (no Kubernetes skill in the list) | Matched javascript, python. Caption: "Not recognized and left out: kubernets, sq, htlm". 1. Quality Assurance Tester 0.22, 2. Software Developer 0.22, 3. Web Developer 0.21 | Pass |

## Files changed

Nothing failed in the check. After the check, the project owner asked for one change: stop a role with a score of 0.00 from showing as a recommendation. Files changed for it:

- `src/matcher.py`: `recommend` now leaves out roles with a score of 0, so fewer than 3 roles can come back.
- `app.py`: shows the heading "Closest roles" and a note when fewer than 3 roles come back, instead of "Top 3 roles".
- `tests/test_cases.py`: added T24, which checks that `html, css, react` returns fewer than 3 roles and none with a score of 0.
- `README.md`: test count changed from 23 to 24, and step 4 of "How it works" now says roles with a score of 0 are not shown.
- `Build_Status.md`: updated the test count, the screen check, the new behavior and the screenshot open item. Dropped "and under pytest", because pytest was not installed for this check and that claim was not checked again.
- `results/test_cases.csv`: rewritten by the test script, now with 24 rows.

After the change: 24 of 24 tests passed, the evaluation output was unchanged, and the 5 extra inputs were run again with no errors. `data/role_profiles.csv` was not touched.

Files added in this session:

- `Build_Report.md`: this report.
- `results/screenshots/`: the 6 screenshots listed above.
- `docs/DECISIONS.md`: dated entries for this check and the change.

## Problems I could not fix

Nothing failed, so these are open notes for the team, not failed fixes. The 0.00 role problem found in the extra inputs is fixed (see Files changed).

1. `python` does not run on this machine. The Windows Store placeholder answers instead. Use `py`, a virtual environment, or turn off the python entries under "App execution aliases" in Windows Settings. Until then the README command `python --version` fails here.
2. pytest is not in `requirements.txt` and was not installed, so `pytest tests/test_cases.py` was not run in this check.
3. Non-English text is shown badly. Accented letters become a space ("programación" shows as "programaci n"). Entries written only in other scripts, such as Japanese or Russian, are dropped without being listed as not recognized. Matching is not affected, and the README already says the tool is English only.
4. Emoji are removed without a message. This caused no wrong result.
5. Short typos (under 5 letters, such as `htlm` or `sq`) are not corrected. This follows the design in Build_Status.md, but a student who types `htlm` gets no html match.
