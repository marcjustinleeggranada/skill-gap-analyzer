# Final screenshots for Chapter 4

Recaptured on 2026-11-01 from the app running locally (`streamlit run app.py`, Streamlit 1.66.1) at commit `d0897b3`, so every image shows the reworded draft notice: "The role profiles are drafts. When the source pages were read, 128 of the 240 role skills were backed by 2 or more sources. Since then 30 of the 54 source pages have closed, so some skills cannot be rechecked." The inputs, roles, scores and skill lists are the same as in the first capture. Each image is a PNG, 1440 px wide, taken with headless Chromium through Playwright, so no browser window frame is included. The Streamlit developer toolbar (Deploy button and main menu) was hidden with a style rule during capture. The app code was not changed. Skills were picked from the "Skills you have" list, as a user would.

| File | What it shows |
|---|---|
| `fig2_input_screen.png` | The input screen before any entry: title, description, the draft notice, the "Skills you have" list opened to show the first skills, the typed box and the Analyze button. |
| `fig3_results_top3.png` | A Software Developer demo input (java, python, object-oriented programming, data structures, algorithms, git). The screen shows "Top 3 roles": 1. Software Developer, score 0.52; 2. Quality Assurance Tester, 0.15; 3. Cybersecurity Analyst, 0.07. Each role lists its matched skills and its missing skills, most role-specific first. The guidance line is at the bottom. |
| `fig4_empty_warning.png` | Analyze pressed with nothing selected or typed. The warning reads: "No skills were entered. Select at least one skill from the list or type a skill name, then press Analyze." |
| `fig5_zero_score_hidden.png` | Input html, css, react. Only 2 of the 8 roles share a skill with it, so the screen shows "Closest roles", the note "Only 2 of the 8 roles share a skill with your input. Roles with a score of 0 are not shown.", then Web Developer (0.39) and Quality Assurance Tester (0.11). |
| `fig6_miss_m04.png` | Mock profile M04 from `data/student_profiles_MOCK.csv` (python, javascript, git, ci/cd, docker, unit testing, sql, technical documentation, agile; true role Software Developer). Quality Assurance Tester is ranked first. Both it and Software Developer display 0.48; the unrounded scores are 0.4846 and 0.4831. Web Developer is third at 0.37. This is a top-1 miss: the true role is second, still inside the top 3. |

Scores are cosine similarity between the student's skills and each role profile, on a scale of 0 to 1.

Image sizes in pixels (width x height): `fig2_input_screen.png` 1440 x 900, `fig3_results_top3.png` 1440 x 1706, `fig4_empty_warning.png` 1440 x 900, `fig5_zero_score_hidden.png` 1440 x 1430, `fig6_miss_m04.png` 1440 x 1611. Each height is the height of the page content, except `fig2`, which is one 900 px screen with the list open.
