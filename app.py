"""Streamlit screen for the Skill Gap Analyzer.

Run with: streamlit run app.py
Nothing the user enters is saved or logged.
"""
import streamlit as st

from src import skill_input
from src.matcher import RoleMatcher

st.set_page_config(page_title="Skill Gap Analyzer", layout="centered")


@st.cache_resource
def load_resources():
    return RoleMatcher(), skill_input.load_skills(), skill_input.load_synonyms()


matcher, skills, synonyms = load_resources()

st.title("Skill Gap Analyzer")
st.write(
    "Select the IT (Information Technology) skills you have. The Matching module "
    "compares them with 8 IT role profiles using TF-IDF (Term Frequency-Inverse "
    "Document Frequency) and cosine similarity. It lists the 3 closest roles and "
    "the skills you still need for each."
)
if matcher.unverified:
    st.info(
        "The role profiles are drafts. When the source pages were read, 128 of the "
        "240 role skills were backed by 2 or more sources. Since then 30 of the 54 "
        "source pages have closed, so some skills cannot be rechecked."
    )

selected = st.multiselect("Skills you have", options=sorted(skills))
typed = st.text_input(
    "Other skills (separate with commas)",
    placeholder="for example: py, postgres, ms excel",
)

if st.button("Analyze"):
    student_skills, unrecognized = skill_input.combine(selected, typed, skills, synonyms)

    if not student_skills:
        st.warning(
            "No skills were entered. Select at least one skill from the list or "
            "type a skill name, then press Analyze."
        )
        if unrecognized:
            st.caption("Not recognized: " + ", ".join(unrecognized))
    else:
        results = matcher.recommend(student_skills, top_n=3)
        if unrecognized:
            st.caption("Not recognized and left out: " + ", ".join(unrecognized))
        if not results:
            st.warning(
                "None of the skills you entered appear in the 8 role profiles, "
                "so no role can be scored. Add more skills."
            )
        else:
            if len(results) == 3:
                st.subheader("Top 3 roles")
            else:
                st.subheader("Closest roles")
                st.caption(
                    f"Only {len(results)} of the 8 roles share a skill with your input. "
                    "Roles with a score of 0 are not shown."
                )
            for rank, item in enumerate(results, start=1):
                st.markdown(f"### {rank}. {item['role']}")
                st.write(f"Cosine similarity score: {item['score']:.2f} (scale 0 to 1)")
                matched = [s for s, _ in item["matched"]]
                missing = [s for s, _ in item["missing"]]
                st.write("Matched skills: " + (", ".join(matched) if matched else "none"))
                st.write(
                    "Missing skills, most role-specific first: "
                    + (", ".join(missing) if missing else "none")
                )
            st.caption(
                "This output is guidance for study planning. It is not a hiring decision."
            )
