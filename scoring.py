"""
ARKHEIA-CPS — Scoring Utilities
Shared functions for weighted risk score computation and level mapping.
"""
from __future__ import annotations


def compute_weighted_score(dimension_scores: dict, weights: dict) -> float:
    """
    Compute overall risk score as weighted average of dimension scores.
    All scores and weights are 0–100 / 0.0–1.0 respectively.
    Returns a float 0–100.
    """
    total  = 0.0
    w_sum  = 0.0
    for dim, weight in weights.items():
        score  = float(dimension_scores.get(dim, 0.0))
        total += score * weight
        w_sum += weight

    if w_sum == 0:
        return 0.0

    return round(min(100.0, total / w_sum * (1 / max(w_sum, 1)) * w_sum), 2)


def score_to_risk_level(score: float) -> str:
    """Map numeric risk score to GREEN / YELLOW / RED."""
    if score >= 55:
        return "RED"
    if score >= 25:
        return "YELLOW"
    return "GREEN"
