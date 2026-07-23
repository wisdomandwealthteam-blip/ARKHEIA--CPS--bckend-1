from .schemas import HousingRuleSet
from .sentinels import Sentinel

DEFAULT_HOUSING = HousingRuleSet(
    state_code="DEFAULT",
    max_security_deposit_months=Sentinel.NO_CAP,
    landlord_entry_notice_hours=Sentinel.NO_NOTICE_REQUIRED,
    max_late_fee_pct=Sentinel.NO_CAP,
    last_reviewed=None,
    notes="Placeholder default; requires attorney review before real-world use.",
)

HOUSING_RULES: dict[str, HousingRuleSet] = {
    "DEFAULT": DEFAULT_HOUSING,
    "GA": HousingRuleSet(
        state_code="GA",
        max_security_deposit_months=2,
        landlord_entry_notice_hours=24,
        max_late_fee_pct=0.10,
        last_reviewed=None,
        notes="Unverified; jurisdiction-specific details require attorney review.",
    ),
    "TX": HousingRuleSet(
        state_code="TX",
        max_security_deposit_months=Sentinel.NO_CAP,
        landlord_entry_notice_hours=Sentinel.NO_NOTICE_REQUIRED,
        max_late_fee_pct=Sentinel.NO_CAP,
        last_reviewed=None,
        notes="Unverified; jurisdiction-specific details require attorney review.",
    ),
    "FL": HousingRuleSet(
        state_code="FL",
        max_security_deposit_months=Sentinel.NO_CAP,
        landlord_entry_notice_hours=Sentinel.NO_NOTICE_REQUIRED,
        max_late_fee_pct=Sentinel.NO_CAP,
        last_reviewed=None,
        notes="Stub entry; requires attorney review.",
    ),
    "CA": HousingRuleSet(
        state_code="CA",
        max_security_deposit_months=Sentinel.NO_CAP,
        landlord_entry_notice_hours=Sentinel.NO_NOTICE_REQUIRED,
        max_late_fee_pct=Sentinel.NO_CAP,
        last_reviewed=None,
        notes="Stub entry; requires attorney review.",
    ),
    "NY": HousingRuleSet(
        state_code="NY",
        max_security_deposit_months=Sentinel.NO_CAP,
        landlord_entry_notice_hours=Sentinel.NO_NOTICE_REQUIRED,
        max_late_fee_pct=Sentinel.NO_CAP,
        last_reviewed=None,
        notes="Stub entry; requires attorney review.",
    ),
}
