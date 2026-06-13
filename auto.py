"""
ARKHEIA-CPS — AUTO Contract Model
FIA entity for auto contracts including Perfection Law date tracking.
"""
import uuid
from sqlalchemy import (
    Column, String, Integer, SmallInteger, Numeric,
    Date, DateTime, ForeignKey, JSON, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base


class AutoContractDetails(Base):
    __tablename__ = "auto_contract_details"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False, unique=True)

    # ── Vehicle Identity ──────────────────────────────────────
    vehicle_vin   = Column(String(17))
    vehicle_year  = Column(SmallInteger)
    vehicle_make  = Column(String(100))
    vehicle_model = Column(String(100))
    vehicle_mileage = Column(Integer)
    vehicle_msrp    = Column(Numeric(12, 2))

    # ── Critical Dates (Perfection Law) ──────────────────────
    purchase_date               = Column(Date)   # date consumer took possession / signed
    contract_execution_date     = Column(Date)   # date contract was signed
    lien_filing_date            = Column(Date)   # date lien was filed with state
    perfection_date             = Column(Date)   # date lien was legally perfected (notation on title)
    repossession_date           = Column(Date)   # date vehicle was repossessed (if applicable)
    notice_of_default_date      = Column(Date)   # date lender sent default notice
    right_to_cure_notice_date   = Column(Date)   # date right-to-cure notice was sent
    sale_date                   = Column(Date)   # date vehicle was sold at auction
    deficiency_notice_date      = Column(Date)   # date deficiency balance notice was sent

    # ── Lien / Title ─────────────────────────────────────────
    lien_holder_name              = Column(String(255))
    lien_recording_jurisdiction   = Column(String(100))   # state or county
    title_issued_date             = Column(Date)
    title_lien_notation_date      = Column(Date)

    # ── Financial Terms ───────────────────────────────────────
    apr                   = Column(Numeric(6, 4))    # e.g. 0.0699
    term_months           = Column(SmallInteger)
    down_payment          = Column(Numeric(12, 2), default=0)
    base_monthly_payment  = Column(Numeric(12, 2))
    financed_amount       = Column(Numeric(12, 2))
    total_cost            = Column(Numeric(12, 2))
    fees_json             = Column(JSON, default=list)   # [{type, label, amount, disclosed}]
    add_ons_json          = Column(JSON, default=list)   # [{type, label, price, optional, itemized}]

    contract = relationship("Contract", back_populates="auto_details")
