from typing import Dict, Any, List, Tuple

from .registry import lookup
from .statutes import build_statute_list


def get_auto_rules(state: str, strict: bool = False) -> Tuple[Dict[str, Any], bool]:
    rules_obj, used_default = lookup("auto", state, strict=strict)
    rules_dict: Dict[str, Any] = {
        "state_code": rules_obj.state_code,
        "deficiency_notice_days": rules_obj.deficiency_notice_days,
        "repossession_notice_days": rules_obj.repossession_notice_days,
        "last_reviewed": rules_obj.last_reviewed,
        "notes": rules_obj.notes,
    }
    return rules_dict, used_default


def get_housing_rules(state: str, strict: bool = False) -> Tuple[Dict[str, Any], bool]:
    rules_obj, used_default = lookup("housing", state, strict=strict)
    rules_dict: Dict[str, Any] = {
        "state_code": rules_obj.state_code,
        "max_security_deposit_months": rules_obj.max_security_deposit_months,
        "landlord_entry_notice_hours": rules_obj.landlord_entry_notice_hours,
        "max_late_fee_pct": rules_obj.max_late_fee_pct,
        "last_reviewed": rules_obj.last_reviewed,
        "notes": rules_obj.notes,
    }
    return rules_dict, used_default


def get_auto_statutes(state: str, strict: bool = False) -> Tuple[List[Dict[str, Any]], bool]:
    rules_obj, used_default = lookup("auto", state, strict=strict)
    statutes = build_statute_list("auto", rules_obj)
    return statutes, used_default


def get_housing_statutes(state: str, strict: bool = False) -> Tuple[List[Dict[str, Any]], bool]:
    rules_obj, used_default = lookup("housing", state, strict=strict)
    statutes = build_statute_list("housing", rules_obj)
    return statutes, used_default
