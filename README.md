# Skill Gap Analyzer

TF-IDF (Term Frequency-Inverse Document Frequency)-Based Skill Gap Analysis and IT (Information Technology) Job Role Recommendation System for IT Students.

Course: IT Elective 1 (Artificial Intelligence), Group 8, BSIT (Bachelor of Science in Information Technology) 3-1. Instructor: Engr. Ian Domel Aspera.

A student selects the IT skills they have from a list of 112 skills. The Matching module compares those skills with 8 IT role profiles using TF-IDF and cosine similarity. The screen shows the top 3 roles, the similarity score, the matched skills and the missing skills for each role. The output is guidance for study planning, not a hiring decision.

## Status of the data

- The 8 role profiles in `data/role_profiles.csv` are drafts. Every row is marked `UNVERIFIED` in the `source` column. The team must check each skill against a real job posting or curriculum and write the reference before the paper cites the profiles.
- `data/student_profiles_SAMPLE.csv` holds 30 made-up profiles. Any accuracy computed from it only checks that the code runs. It is not the project's accuracy. Every report built from it starts with the line "SAMPLE DATA, NOT A PROJECT RESULT".
- To use real profiles, save them as `data/student_profiles.csv` (columns: `profile_id`, `skills`, `true_role`; skills separated by semicolons). The evaluation code picks that file first and needs no change.

## Install

Python 3.10 or newer.

```
pip install -r requirements.txt
```

## Run the screen

```
streamlit run app.py
```

Select skills from the list, type extra skills if needed (for example `py`, `postgres`, `ms excel`), then press Analyze. Nothing you enter is saved or logged.

## Run the evaluation

```
python -m src.evaluate
python -m src.evaluate --profiles data/student_profiles.csv
```

This prints and saves:

- `results/accuracy.json`: top-3 accuracy (profiles whose true role is in the top 3 roles, divided by all profiles), top-1 accuracy, the random baseline (37.5%, which is 3 of 8 roles), and the most-common-roles baseline.
- `results/errors.csv`: each profile where the true role is not ranked first, with the recommended top 3 and the likely cause. The `error_type` column separates top-3 misses from top-1 misses.
- `results/confusion.csv`: true role against the role ranked first.

One wrong result moves top-3 accuracy by about 3.3 points on 30 profiles, so the accuracy figure is rough.

## Run the tests

```
python tests/test_cases.py
```

This runs 24 test cases and writes `results/test_cases.csv` with the input, expected result, actual result and pass or fail for each. `pytest tests/test_cases.py` runs the same cases.

## How it works

1. The Matching module builds one document per role from its skill list.
2. It fits a scikit-learn `TfidfVectorizer` on the 8 documents. A custom analyzer keeps multi-word skills such as "machine learning" as single terms.
3. It converts the student's skills with the same fitted vocabulary.
4. It ranks roles by cosine similarity and returns the top 3. A role with a score of 0 shares no skill with the student and is not shown, so fewer than 3 roles can appear.
5. The Skill Gap module lists the role skills the student lacks, ordered by TF-IDF weight, so the most role-specific skills come first.

No model is trained and no answer is stored. Every score comes from the skills shared between the student and the role. Skills that appear in many roles (for example teamwork) get a low weight. Skills that appear in one role (for example penetration testing) get a high weight.

The Skill Input module cleans typed text, applies the synonym table in `data/synonyms.csv`, corrects close misspellings of words with 5 or more letters, and keeps only terms found in `data/skills.csv`.

## Files

```
app.py                 Streamlit screen
src/skill_input.py     Skill Input module
src/matcher.py         Matching module
src/skill_gap.py       Skill Gap module
src/evaluate.py        evaluation
tests/test_cases.py    test cases
data/                  skills, synonyms, role profiles, sample student profiles
results/               evaluation and test output
requirements.txt       pinned library versions
```

To change a role or its skills, edit `data/role_profiles.csv`. Every skill in it must also appear in `data/skills.csv`.

## Skill names that are acronyms

- api: application programming interface (the skill is named "rest api", REST is Representational State Transfer)
- ci/cd: continuous integration and continuous delivery
- css: Cascading Style Sheets
- dhcp: Dynamic Host Configuration Protocol
- dns: Domain Name System
- etl: extract, transform, load
- html: HyperText Markup Language
- siem: security information and event management
- sql: Structured Query Language
- tcp/ip: Transmission Control Protocol and Internet Protocol
- vlan: virtual local area network
- vpn: virtual private network

## Limits

- The role profiles are unverified drafts until the team adds real sources.
- Matching uses skill names only. It does not weigh how well a student knows a skill.
- Roles with many shared skills (Software Developer and Web Developer, Network Administrator and IT Support Specialist) are easy to confuse. Expect errors there.
- English only. No resume reading, live job scraping or salary prediction.

## Demo script

1. Start the screen with `streamlit run app.py`.
2. Select `html`, `css`, `react` and `git`. Type `py, js` in the other box. Press Analyze.
3. Show the top 3 roles, the scores, the matched skills and the missing skills.
4. Show one limitation: select only `teamwork`, `communication` and `problem solving`. The scores stay low because these skills appear in every role.

## Credits

- scikit-learn (TF-IDF and cosine similarity)
- pandas (reading CSV files)
- Streamlit (web screen)
- Python standard library `difflib` (close spelling matches)
- Role skills, skill list and synonyms: drafted from general knowledge. Not yet checked against postings.
