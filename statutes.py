from typing import Any, Dict, List

from .sentinels import Sentinel


def build_statute_list(domain: str, rules: object) -> List[Dict[str, Any]]:
    """
    Shared statute-list derivation.

    Legally neutral: all citations are placeholders and marked as requiring attorney review.
    """
    entries: List[Dict[str, Any]] = []

    if domain == "auto":
        entries.append(
            {
                "jurisdiction": "State",
                "citation": Sentinel.UNVERIFIED_STATUTE.value,
                "description": "State-level auto deficiency and repossession rules.",
                "status": Sentinel.REQUIRES_ATTORNEY_REVIEW.value,
            }
        )
    elif domain == "housing":
        entries.append(
            {
                "jurisdiction": "State",
                "citation": Sentinel.UNVERIFIED_STATUTE.value,
                "description": "State-level landlord-tenant rules (deposit, entry, late fees).",
                "status": Sentinel.REQUIRES_ATTORNEY_REVIEW.value,
            }
        )

    entries.append(
        {
            "jurisdiction": "Federal",
            "citation": Sentinel.UNVERIFIED_STATUTE.value,
            "description": "Relevant federal consumer-protection framework (placeholder).",
            "status": Sentinel.REQUIRES_ATTORNEY_REVIEW.value,
        }
    )

    return entries
