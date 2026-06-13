"""
ARKHEIA-CPS — HOUSING Contract Model
Full FIA entity for residential lease agreements.
"""
import uuid
from sqlalchemy import (
    Column, String, Integer, SmallInteger, Numeric,
    Boolean, Text, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class HousingContractDetails(Base):
    __tablename__ = "housing_contract_details"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False, unique=True)

    # ── Property Identity ─────────────────────────────────────
    property_address  = Column(Text, nullable=False)
    unit_number       = Column(String(50))
    property_type     = Column(String(50))    # apartment, single_family, duplex, condo, townhouse
    bedrooms          = Column(SmallInteger)
    bathrooms         = Column(Numeric(3, 1))
    square_footage    = Column(Integer)
    lease_start_date  = Column(String(20))    # ISO date string
    lease_end_date    = Column(String(20))
    lease_term_months = Column(SmallInteger)

    # ── Financial Terms ───────────────────────────────────────
    base_monthly_rent           = Column(Numeric(10, 2), nullable=False)
    rent_due_day                = Column(SmallInteger, default=1)    # day of month
    grace_period_days           = Column(SmallInteger, default=0)
    late_fee_amount             = Column(Numeric(8, 2), default=0)
    late_fee_type               = Column(String(20), default="flat")  # flat | percentage
    late_fee_percentage         = Column(Numeric(5, 2))               # if percentage type
    rent_increase_clause_text   = Column(Text)
    rent_increase_cap_percentage = Column(Numeric(5, 2))
    rent_increase_frequency     = Column(String(30))    # annual | renewal | discretionary

    # ── Move-In Costs ─────────────────────────────────────────
    security_deposit_amount   = Column(Numeric(10, 2), default=0)
    security_deposit_type     = Column(String(20), default="refundable")  # refundable | non_refundable | mixed
    first_month_rent_due      = Column(Boolean, default=True)
    last_month_rent_due       = Column(Boolean, default=False)
    application_fee_amount    = Column(Numeric(8, 2), default=0)
    admin_fee_amount          = Column(Numeric(8, 2), default=0)
    other_upfront_fees_json   = Column(JSON, default=list)   # [{label, amount}]

    # ── Recurring Fees ────────────────────────────────────────
    recurring_fees_json = Column(JSON, default=list)  # [{label, amount, frequency, mandatory}]

    # ── Utilities ─────────────────────────────────────────────
    electricity_responsibility = Column(String(20))   # tenant | landlord | included | split
    water_responsibility       = Column(String(20))
    gas_responsibility         = Column(String(20))
    trash_responsibility       = Column(String(20))
    internet_responsibility    = Column(String(20))
    utility_billing_method     = Column(String(50))   # direct | RUBS | flat_fee | submetered
    utility_fee_items_json     = Column(JSON, default=list)  # [{label, amount, method}]

    # ── Maintenance ───────────────────────────────────────────
    landlord_responsible_items_json  = Column(JSON, default=list)  # [item descriptions]
    tenant_responsible_items_json    = Column(JSON, default=list)
    emergency_response_time_hours    = Column(SmallInteger)
    standard_repair_response_time_days = Column(SmallInteger)
    maintenance_clause_text          = Column(Text)

    # ── Legal / Enforcement ───────────────────────────────────
    lease_clauses_json              = Column(JSON, default=list)   # [{category, text, flags}]
    early_termination_penalty_amount = Column(Numeric(10, 2))
    early_termination_penalty_type   = Column(String(30))          # flat | months_of_rent
    early_termination_months         = Column(Numeric(4, 1))       # if months_of_rent type
    notice_required_days_by_tenant   = Column(SmallInteger)
    notice_required_days_by_landlord = Column(SmallInteger)
    automatic_renewal               = Column(Boolean, default=False)
    automatic_renewal_notice_days   = Column(SmallInteger)
    termination_clause_text         = Column(Text)
    late_payment_eviction_trigger_days = Column(SmallInteger)
    eviction_notice_type            = Column(String(50))   # pay_or_quit | unconditional_quit | cure_or_quit
    eviction_notice_days            = Column(SmallInteger)
    eviction_clause_text            = Column(Text)
    arbitration_required            = Column(Boolean, default=False)
    dispute_venue                   = Column(String(100))
    dispute_fee_sharing_terms       = Column(String(100))
    dispute_resolution_clause_text  = Column(Text)

    contract = relationship("Contract", back_populates="housing_details")
