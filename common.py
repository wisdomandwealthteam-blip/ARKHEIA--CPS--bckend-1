"""
ARKHEIA-CPS — Common Models
Shared entities used across AUTO and HOUSING verticals.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Numeric, Boolean, DateTime,
    Text, Enum as SAEnum, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base
import enum


class VerticalType(str, enum.Enum):
    AUTO    = "AUTO"
    HOUSING = "HOUSING"


class Contract(Base):
    __tablename__ = "contracts"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type                = Column(SAEnum(VerticalType), nullable=False)
    jurisdiction_state  = Column(String(2), nullable=False)       # e.g. "GA"
    jurisdiction_city   = Column(String(100))
    raw_file_path       = Column(Text)                            # S3/local path if uploaded
    upload_timestamp    = Column(DateTime, default=datetime.utcnow)
    analysis_timestamp  = Column(DateTime)

    # Relationships
    consumer            = relationship("Consumer",     back_populates="contracts", uselist=False)
    counterparty        = relationship("Counterparty", back_populates="contracts", uselist=False)
    auto_details        = relationship("AutoContractDetails",    back_populates="contract", uselist=False)
    housing_details     = relationship("HousingContractDetails", back_populates="contract", uselist=False)
    analysis_result     = relationship("AnalysisResult",         back_populates="contract", uselist=False)


class Consumer(Base):
    __tablename__ = "consumers"

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id             = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False)
    name                    = Column(String(255), nullable=False)
    email                   = Column(String(255))
    phone                   = Column(String(30))
    reported_monthly_income = Column(Numeric(12, 2))
    net_monthly_income      = Column(Numeric(12, 2))
    household_size          = Column(Integer)
    credit_band             = Column(String(20))     # EXCELLENT/GOOD/FAIR/POOR/DEEP_SUBPRIME

    contracts               = relationship("Contract", back_populates="consumer")


class Counterparty(Base):
    """Dealer, Lender, Landlord — whoever is on the other side of the contract."""
    __tablename__ = "counterparties"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False)
    name        = Column(String(255), nullable=False)
    entity_type = Column(String(50))    # individual, LLC, bank, corporation
    email       = Column(String(255))
    phone       = Column(String(30))
    address     = Column(Text)
    license_number = Column(String(100))

    contracts   = relationship("Contract", back_populates="counterparty")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id                              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id                     = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False, unique=True)
    vertical                        = Column(SAEnum(VerticalType), nullable=False)

    # Overall
    overall_risk_score              = Column(Numeric(5, 2), nullable=False)   # 0–100
    risk_level                      = Column(String(10))                      # GREEN/YELLOW/RED

    # AUTO dimension scores
    affordability_score             = Column(Numeric(5, 2))
    fee_score                       = Column(Numeric(5, 2))
    term_score                      = Column(Numeric(5, 2))
    vehicle_safety_score            = Column(Numeric(5, 2))
    enforcement_score               = Column(Numeric(5, 2))
    perfection_risk_score           = Column(Numeric(5, 2))

    # HOUSING dimension scores
    lease_term_score                = Column(Numeric(5, 2))
    habitability_score              = Column(Numeric(5, 2))
    eviction_safety_score           = Column(Numeric(5, 2))

    # Shared results
    triggered_alerts_json           = Column(JSON, default=list)   # [{code, severity, message}]
    statutes_json                   = Column(JSON, default=list)   # [{jurisdiction, citation, description}]
    explanations_json               = Column(JSON, default=list)   # [plain-language strings]
    pem_evaluations_json            = Column(JSON, default=list)   # OIA-PEM pattern results

    created_at                      = Column(DateTime, default=datetime.utcnow)

    contract                        = relationship("Contract", back_populates="analysis_result")
