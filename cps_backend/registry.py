from typing import Literal, Tuple

from .auto import AUTO_RULES
from .exceptions import StateNotSupportedError
from .housing import HOUSING_RULES

Domain = Literal["auto", "housing"]

SUPPORTED_STATES: set[str] = {"GA", "TX", "FL", "CA", "NY"}


def lookup(
    domain: Domain,
    state: str,
    strict: bool = False,
) -> Tuple[object, bool]:
    state_code = state.upper()

    if state_code not in SUPPORTED_STATES and strict:
        raise StateNotSupportedError(f"Unsupported state: {state_code}")

    if domain == "auto":
        table = AUTO_RULES
    elif domain == "housing":
        table = HOUSING_RULES
    else:
        raise ValueError(f"Unknown domain: {domain}")

    if state_code in table:
        return table[state_code], False

    return table["DEFAULT"], True
