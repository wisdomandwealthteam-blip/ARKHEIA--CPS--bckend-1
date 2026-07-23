from .schemas import AutoRuleSet

DEFAULT_AUTO = AutoRuleSet(
    state_code="DEFAULT",
    deficiency_notice_days=0,
    repossession_notice_days=0,
    last_reviewed=None,
    notes="Placeholder default; requires attorney review before real-world use.",
)

AUTO_RULES: dict[str, AutoRuleSet] = {
    "DEFAULT": DEFAULT_AUTO,
    "GA": AutoRuleSet(
        state_code="GA",
        deficiency_notice_days=10,
        repossession_notice_days=0,
        last_reviewed=None,
        notes="Unverified; jurisdiction-specific details require attorney review.",
    ),
    "TX": AutoRuleSet(
        state_code="TX",
        deficiency_notice_days=0,
        repossession_notice_days=0,
        last_reviewed=None,
        notes="Unverified; jurisdiction-specific details require attorney review.",
    ),
    "FL": AutoRuleSet(
        state_code="FL",
        deficiency_notice_days=0,
        repossession_notice_days=0,
        last_reviewed=None,
        notes="Stub entry; requires attorney review.",
    ),
    "CA": AutoRuleSet(
        state_code="CA",
        deficiency_notice_days=0,
        repossession_notice_days=0,
        last_reviewed=None,
        notes="Stub entry; requires attorney review.",
    ),
    "NY": AutoRuleSet(
        state_code="NY",
        deficiency_notice_days=0,
        repossession_notice_days=0,
        last_reviewed=None,
        notes="Stub entry; requires attorney review.",
    ),
}
