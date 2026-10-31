"""Matching module.

Fits a scikit-learn TfidfVectorizer (TF-IDF: Term Frequency-Inverse Document
Frequency) on one document per role. Ranks roles by cosine similarity between
the student's skills and each role vector. No model training, no stored answers.
"""
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src import skill_gap

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_SEP = "|"


def _split_terms(document):
    """Analyzer: a document is skills joined by "|", so multi-word skills
    such as "machine learning" stay as single terms."""
    return [t for t in document.split(_SEP) if t]


class RoleMatcher:
    def __init__(self, role_profiles_path=None):
        path = role_profiles_path or DATA_DIR / "role_profiles.csv"
        df = pd.read_csv(path)
        df["role"] = df["role"].str.strip()
        df["skill"] = df["skill"].str.strip().str.lower()
        self.role_skills = {
            role: list(dict.fromkeys(group["skill"]))
            for role, group in df.groupby("role", sort=True)
        }
        self.roles = list(self.role_skills)
        self.unverified = bool((df["source"].astype(str).str.upper() == "UNVERIFIED").any())

        documents = [_SEP.join(self.role_skills[r]) for r in self.roles]
        self.vectorizer = TfidfVectorizer(analyzer=_split_terms)
        self.role_matrix = self.vectorizer.fit_transform(documents)
        self.vocabulary = set(self.vectorizer.vocabulary_)
        terms = self.vectorizer.get_feature_names_out()
        # weight of each skill inside each role vector
        self.role_weights = {}
        for i, role in enumerate(self.roles):
            row = self.role_matrix[i]
            self.role_weights[role] = {
                terms[j]: float(v) for j, v in zip(row.indices, row.data)
            }

    def score_all(self, student_skills):
        """Return {role: cosine similarity} for every role.

        Skills outside the role vocabulary are ignored. If none are inside it,
        all scores are 0.0.
        """
        known = [s for s in dict.fromkeys(student_skills) if s in self.vocabulary]
        if not known:
            return {r: 0.0 for r in self.roles}
        vec = self.vectorizer.transform([_SEP.join(known)])
        sims = cosine_similarity(vec, self.role_matrix)[0]
        return {r: float(s) for r, s in zip(self.roles, sims)}

    def recommend(self, student_skills, top_n=3):
        """Return the top roles as a list of dicts, best first.

        Each dict has role, score, matched (shared skills) and missing
        (role skills the student lacks). Roles with a score of 0 share no
        skill with the student and are left out, so fewer than top_n roles
        can come back. Returns [] when no skill matches any role.
        """
        scores = self.score_all(student_skills)
        scored = [(r, s) for r, s in scores.items() if s > 0]
        ranked = sorted(scored, key=lambda kv: (-kv[1], kv[0]))[:top_n]
        student = set(student_skills)
        results = []
        for role, score in ranked:
            results.append({
                "role": role,
                "score": round(score, 4),
                "matched": skill_gap.matched_skills(self, role, student),
                "missing": skill_gap.missing_skills(self, role, student),
            })
        return results
