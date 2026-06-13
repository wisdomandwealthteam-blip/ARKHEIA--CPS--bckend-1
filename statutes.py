"""
ARKHEIA-CPS — Statute Mapping
State-specific consumer protection rules and citations.
Architecture designed for real statute database integration.
"""
from __future__ import annotations
from typing import List


# ── AUTO Perfection Rules ─────────────────────────────────────

AUTO_PERFECTION_RULES: dict = {
    "GA": {
        "expected_max_days": 30,
        "min_cure_days":     10,
        "perfection_statute": "O.C.G.A. § 40-3-53 (Certificate of Title Act — Lien Notation)",
        "repo_statute":       "O.C.G.A. § 11-9-609 (UCC Article 9 — Self-Help Repossession)",
        "notice_statute":     "O.C.G.A. § 10-1-36 (Motor Vehicle Sales Finance Act — Default Notice)",
        "cure_statute":       "O.C.G.A. § 10-1-36 (Right to Cure Notice — 10 Days Required)",
        "deficiency_statute": "O.C.G.A. § 10-1-36 (Deficiency Notice — 10 Days After Sale)",
        "fbpa_statute":       "O.C.G.A. § 10-1-390 (Fair Business Practices Act)",
    },
    "FL": {
        "expected_max_days": 30,
        "min_cure_days":     20,
        "perfection_statute": "Fla. Stat. § 319.27 (Certificate of Title — Lien)",
        "repo_statute":       "Fla. Stat. § 679.609 (UCC Art. 9 — Repossession)",
        "notice_statute":     "Fla. Stat. § 537.012 (Consumer Finance Act — Default Notice)",
        "cure_statute":       "Fla. Stat. § 537.012 (Right to Cure)",
        "deficiency_statute": "Fla. Stat. § 679.626",
        "fbpa_statute":       "Fla. Stat. § 501.201 (FDUTPA)",
    },
    "TX": {
        "expected_max_days": 20,
        "min_cure_days":     10,
        "perfection_statute": "Tex. Transp. Code § 501.111 (Certificate of Title — Lien)",
        "repo_statute":       "Tex. Bus. & Com. Code § 9.609 (UCC Art. 9)",
        "notice_statute":     "Tex. Fin. Code § 348.408 (Motor Vehicle Installment Sales)",
        "cure_statute":       "Tex. Fin. Code § 348.408",
        "deficiency_statute": "Tex. Fin. Code § 348.410",
        "fbpa_statute":       "Tex. Bus. & Com. Code § 17.41 (DTPA)",
    },
    "DEFAULT": {
        "expected_max_days": 30,
        "min_cure_days":     10,
        "perfection_statute": "UCC Article 9 § 9-310 (Filing to Perfect Security Interest)",
        "repo_statute":       "UCC Article 9 § 9-609 (Self-Help Repossession)",
        "notice_statute":     "UCC Article 9 § 9-611 (Notification Before Disposition)",
        "cure_statute":       "State-specific right-to-cure statute",
        "deficiency_statute": "UCC Article 9 § 9-626",
        "fbpa_statute":       "FTC Act § 5 (Unfair or Deceptive Acts)",
    },
}

# ── HOUSING Tenant Rules ──────────────────────────────────────

HOUSING_TENANT_RULES: dict = {
    "GA": {
        "max_security_deposit_months": None,    # Georgia has no statutory cap
        "min_grace_period_days":       0,
        "max_late_fee_pct":            0.05,    # No statutory cap; 5% is common guidance
        "notice_to_quit_days":         60,      # For month-to-month
        "eviction_notice_days":        3,       # Pay or quit
        "landlord_entry_notice_hours": 24,
        "habitability_statute":        "O.C.G.A. § 44-7-13 (Landlord Duty to Repair)",
        "security_deposit_statute":    "O.C.G.A. § 44-7-30 et seq. (Security Deposits)",
        "eviction_statute":            "O.C.G.A. § 44-7-50 et seq. (Dispossessory Proceedings)",
        "consumer_protection_statute": "O.C.G.A. § 10-1-390 (FBPA)",
        "retaliation_statute":         "O.C.G.A. § 44-7-24 (Retaliatory Eviction)",
    },
    "CA": {
        "max_security_deposit_months": 2,       # Unfurnished
        "min_grace_period_days":       3,
        "max_late_fee_pct":            0.0,     # No percentage cap; must be "reasonable"
        "notice_to_quit_days":         30,
        "eviction_notice_days":        3,
        "landlord_entry_notice_hours": 24,
        "habitability_statute":        "Cal. Civ. Code § 1941",
        "security_deposit_statute":    "Cal. Civ. Code § 1950.5",
        "eviction_statute":            "Cal. Code Civ. Proc. § 1161",
        "consumer_protection_statute": "Cal. Bus. & Prof. Code § 17200 (UCL)",
        "retaliation_statute":         "Cal. Civ. Code § 1942.5",
    },
    "NY": {
        "max_security_deposit_months": 1,
        "min_grace_period_days":       5,
        "max_late_fee_pct":            0.05,
        "notice_to_quit_days":         30,
        "eviction_notice_days":        14,
        "landlord_entry_notice_hours": 24,
        "habitability_statute":        "N.Y. Real Prop. Law § 235-b",
        "security_deposit_statute":    "N.Y. Gen. Oblig. Law § 7-108",
        "eviction_statute":            "N.Y. Real Prop. Acts Law § 701",
        "consumer_protection_statute": "N.Y. Gen. Bus. Law § 349",
        "retaliation_statute":         "N.Y. Real Prop. Law § 223-b",
    },
    "TX": {
        "max_security_deposit_months": None,
        "min_grace_period_days":       2,
        "max_late_fee_pct":            0.12,    # 12% of monthly rent
        "notice_to_quit_days":         30,
        "eviction_notice_days":        3,
        "landlord_entry_notice_hours": None,    # No statutory notice required
        "habitability_statute":        "Tex. Prop. Code § 92.052",
        "security_deposit_statute":    "Tex. Prop. Code § 92.101",
        "eviction_statute":            "Tex. Prop. Code § 24.001",
        "consumer_protection_statute": "Tex. Bus. & Com. Code § 17.41 (DTPA)",
        "retaliation_statute":         "Tex. Prop. Code § 92.331",
    },
    "DEFAULT": {
        "max_security_deposit_months": 2,
        "min_grace_period_days":       3,
        "max_late_fee_pct":            0.05,
        "notice_to_quit_days":         30,
        "eviction_notice_days":        5,
        "landlord_entry_notice_hours": 24,
        "habitability_statute":        "State Landlord-Tenant Act — Implied Warranty of Habitability",
        "security_deposit_statute":    "State Security Deposit Statute",
        "eviction_statute":            "State Eviction / Unlawful Detainer Statute",
        "consumer_protection_statute": "FTC Act § 5",
        "retaliation_statute":         "State Anti-Retaliation Statute",
    },
}

# ── Public API ────────────────────────────────────────────────

def get_auto_perfection_rules(state: str) -> dict:
    """Return state-specific perfection law rules and statute citations."""
    return AUTO_PERFECTION_RULES.get(state.upper(), AUTO_PERFECTION_RULES["DEFAULT"])


def get_housing_tenant_rules(state: str) -> dict:
    """Return state-specific tenant protection rules and statute citations."""
    return HOUSING_TENANT_RULES.get(state.upper(), HOUSING_TENANT_RULES["DEFAULT"])


def get_auto_statutes(state: str) -> List[dict]:
    """Return list of applicable auto statutes for the analysis report."""
    rules = get_auto_perfection_rules(state)
    return [
        {"jurisdiction": state, "citation": rules["perfection_statute"],
         "description": "Lien perfection requirement"},
        {"jurisdiction": state, "citation": rules["repo_statute"],
         "description": "Self-help repossession rules"},
        {"jurisdiction": state, "citation": rules["notice_statute"],
         "description": "Default notice requirement"},
        {"jurisdiction": state, "citation": rules["cure_statute"],
         "description": "Right-to-cure notice requirement"},
        {"jurisdiction": "Federal", "citation": "15 U.S.C. § 1638 (TILA)",
         "description": "Truth in Lending — APR and cost disclosure"},
        {"jurisdiction": "Federal", "citation": "15 U.S.C. § 1691 (ECOA)",
         "description": "Equal Credit Opportunity Act — anti-discrimination"},
    ]


def get_housing_statutes(state: str) -> List[dict]:
    """Return list of applicable housing statutes for the analysis report."""
    rules = get_housing_tenant_rules(state)
    return [
        {"jurisdiction": state, "citation": rules["habitability_statute"],
         "description": "Landlord duty to maintain habitable premises"},
        {"jurisdiction": state, "citation": rules["security_deposit_statute"],
         "description": "Security deposit limits and return requirements"},
        {"jurisdiction": state, "citation": rules["eviction_statute"],
         "description": "Eviction notice and procedure requirements"},
        {"jurisdiction": state, "citation": rules["consumer_protection_statute"],
         "description": "Unfair or deceptive acts in consumer transactions"},
        {"jurisdiction": state, "citation": rules["retaliation_statute"],
         "description": "Protection against retaliatory eviction"},
        {"jurisdiction": "Federal", "citation": "42 U.S.C. § 3604 (Fair Housing Act)",
         "description": "Anti-discrimination in housing"},
    ]
