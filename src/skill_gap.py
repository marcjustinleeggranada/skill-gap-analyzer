"""Skill Gap module.

Lists matched and missing skills for a role, ordered by TF-IDF weight
(most role-specific first). Weights come from the role vectors that the
Matching module fitted.
"""


def _ordered(matcher, role, skills):
    weights = matcher.role_weights[role]
    return sorted(skills, key=lambda s: (-weights.get(s, 0.0), s))


def matched_skills(matcher, role, student_skills):
    """Role skills the student has, heaviest weight first."""
    have = [s for s in matcher.role_skills[role] if s in student_skills]
    return [(s, round(matcher.role_weights[role][s], 4)) for s in _ordered(matcher, role, have)]


def missing_skills(matcher, role, student_skills):
    """Role skills the student lacks, heaviest weight first."""
    lack = [s for s in matcher.role_skills[role] if s not in student_skills]
    return [(s, round(matcher.role_weights[role][s], 4)) for s in _ordered(matcher, role, lack)]
