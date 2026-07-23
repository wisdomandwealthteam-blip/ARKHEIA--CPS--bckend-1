from dataclasses import dataclass, field
from typing import Any, Optional

from .exceptions import SchemaValidationError
from .sentinels import Sentinel


@dataclass(frozen=True)
class AutoRuleSet:
    state_code: str
    deficiency_notice_days: int
    repossession_notice_days: int
    last_reviewed: Optional[str] = field(default=None)
    notes: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        obj: Any = self
        if len(self.state_code) != 2 or not self.state_code.isalpha():
            raise SchemaValidationError(f"Invalid state_code: {self.state_code}")
        if self.deficiency_notice_days < 0:
            raise SchemaValidationError("deficiency_notice_days cannot be negative")
        if self.repossession_notice_days < 0:
            raise SchemaValidationError("repossession_notice_days cannot be negative")


@dataclass(frozen=True)
class HousingRuleSet:
    state_code: str
    max_security_deposit_months: int | Sentinel
    landlord_entry_notice_hours: int | Sentinel
    max_late_fee_pct: float | Sentinel
    last_reviewed: Optional[str] = field(default=None)
    notes: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        obj: Any = self
        if len(self.state_code) != 2 or not self.state_code.isalpha():
            raise SchemaValidationError(f"Invalid state_code: {self.state_code}")

        if isinstance(self.max_security_deposit_months, int):
            if self.max_security_deposit_months < 0:
                raise SchemaValidationError("max_security_deposit_months cannot be negative")
        elif self.max_security_deposit_months is not Sentinel.NO_CAP:
            raise SchemaValidationError("Invalid sentinel for max_security_deposit_months")

        if isinstance(self.landlord_entry_notice_hours, int):
            if self.landlord_entry_notice_hours < 0:
                raise SchemaValidationError("landlord_entry_notice_hours cannot be negative")
        elif self.landlord_entry_notice_hours is not Sentinel.NO_NOTICE_REQUIRED:
            raise SchemaValidationError("Invalid sentinel for landlord_entry_notice_hours")

        if isinstance(self.max_late_fee_pct, float):
            if self.max_late_fee_pct < 0.0:
                raise SchemaValidationError("max_late_fee_pct cannot be negative")
        elif self.max_late_fee_pct is not Sentinel.NO_CAP:
            raise SchemaValidationError("Invalid sentinel for max_late_fee_pct")
