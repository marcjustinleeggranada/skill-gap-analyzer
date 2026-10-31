"""Skill Input module.

Cleans typed skill entries, applies the synonym table and keeps only terms
that appear in data/skills.csv.
"""
import difflib
import re
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Characters kept inside a skill name: letters, digits, space and . + # / -
_ALLOWED = re.compile(r"[^a-z0-9 .+#/\-]")
_SPLIT = re.compile(r"[,;\n]")
# Fuzzy matching is limited to longer words so short terms such as "r" or "sql"
# are never "corrected" into something else.
_FUZZY_MIN_LENGTH = 5
_FUZZY_CUTOFF = 0.8


def load_skills(path=None):
    """Return the list of valid skills from skills.csv."""
    path = path or DATA_DIR / "skills.csv"
    return pd.read_csv(path)["skill"].str.strip().str.lower().tolist()


def load_synonyms(path=None):
    """Return a dict that maps a typed variant to its standard skill."""
    path = path or DATA_DIR / "synonyms.csv"
    df = pd.read_csv(path)
    return {
        str(v).strip().lower(): str(s).strip().lower()
        for v, s in zip(df["variant"], df["standard_skill"])
    }


def normalize(text):
    """Lowercase, drop unsupported characters and collapse spaces."""
    text = str(text).lower()
    text = _ALLOWED.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip(" .-/")
    return text


def resolve_term(term, valid_skills, synonyms):
    """Map one cleaned term to a standard skill, or return None.

    Order: exact skill, synonym table, close spelling match.
    """
    if not term:
        return None
    if term in valid_skills:
        return term
    if term in synonyms:
        return synonyms[term]
    if len(term) >= _FUZZY_MIN_LENGTH:
        close = difflib.get_close_matches(
            term, list(valid_skills) + list(synonyms), n=1, cutoff=_FUZZY_CUTOFF
        )
        if close:
            match = close[0]
            return match if match in valid_skills else synonyms[match]
    return None


def clean_entries(typed_text, valid_skills, synonyms):
    """Clean a typed entry such as "py, javascrpit, !!!".

    Returns (recognized, unrecognized). Both lists keep input order and have
    no duplicates. A non-string value is treated as empty input.
    """
    if not isinstance(typed_text, str):
        return [], []
    valid = set(valid_skills)
    recognized, unrecognized = [], []
    for raw in _SPLIT.split(typed_text):
        term = normalize(raw)
        if not term:
            continue
        skill = resolve_term(term, valid, synonyms)
        if skill is None:
            if term not in unrecognized:
                unrecognized.append(term)
        elif skill not in recognized:
            recognized.append(skill)
    return recognized, unrecognized


def combine(selected, typed_text, valid_skills, synonyms):
    """Merge list selections with typed entries.

    Returns (skills, unrecognized). Selected items also pass through the
    cleaning step, so a bad value in the list cannot reach the Matching module.
    """
    skills = []
    unrecognized = []
    chosen = selected if isinstance(selected, (list, tuple, set)) else []
    for item in chosen:
        rec, unrec = clean_entries(str(item), valid_skills, synonyms)
        for s in rec:
            if s not in skills:
                skills.append(s)
        for u in unrec:
            if u not in unrecognized:
                unrecognized.append(u)
    rec, unrec = clean_entries(typed_text, valid_skills, synonyms)
    for s in rec:
        if s not in skills:
            skills.append(s)
    for u in unrec:
        if u not in unrecognized:
            unrecognized.append(u)
    return skills, unrecognized
