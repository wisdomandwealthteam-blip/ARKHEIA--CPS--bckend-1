"""
ARKHEIA-CPS — FIA Auto Service
Layer 1: Structure all AUTO contract entities into the database.
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.common import Contract, Consumer, Counterparty, VerticalType
from app.models.auto import AutoContractDetails
from app.schemas.auto import AutoContractIn


class FIAAutoService:
    """
    FIA (Formal Identity Architecture) for AUTO contracts.
    Parses structured input and creates all entity records.
    """

    def __init__(self, db: Session):
        self.db = db

    def structure(self, payload: AutoContractIn) -> tuple[Contract, AutoContractDetails]:
        """
        Create Contract + Consumer + Counterparty + AutoContractDetails.
        Returns (contract, auto_details) ORM objects.
        """

        # 1. Base contract
        contract = Contract(
            type=VerticalType.AUTO,
            jurisdiction_state=payload.jurisdiction_state.upper(),
            jurisdiction_city=payload.jurisdiction_city,
            upload_timestamp=datetime.utcnow(),
        )
        self.db.add(contract)
        self.db.flush()

        # 2. Consumer
        consumer = Consumer(
            contract_id=contract.id,
            name=payload.consumer.name,
            email=payload.consumer.email,
            phone=payload.consumer.phone,
            reported_monthly_income=payload.consumer.reported_monthly_income,
            net_monthly_income=payload.consumer.net_monthly_income,
            household_size=payload.consumer.household_size,
            credit_band=payload.consumer.credit_band,
        )
        self.db.add(consumer)

        # 3. Counterparty (dealer/lender)
        counterparty = Counterparty(
            contract_id=contract.id,
            name=payload.counterparty.name,
            entity_type=payload.counterparty.entity_type,
            email=payload.counterparty.email,
            phone=payload.counterparty.phone,
            address=payload.counterparty.address,
            license_number=payload.counterparty.license_number,
        )
        self.db.add(counterparty)

        # 4. Auto details
        auto_details = AutoContractDetails(
            contract_id=contract.id,
            vehicle_vin=payload.vehicle_vin,
            vehicle_year=payload.vehicle_year,
            vehicle_make=payload.vehicle_make,
            vehicle_model=payload.vehicle_model,
            vehicle_mileage=payload.vehicle_mileage,
            vehicle_msrp=payload.vehicle_msrp,
            # Perfection law dates
            purchase_date=payload.purchase_date,
            contract_execution_date=payload.contract_execution_date,
            lien_filing_date=payload.lien_filing_date,
            perfection_date=payload.perfection_date,
            repossession_date=payload.repossession_date,
            notice_of_default_date=payload.notice_of_default_date,
            right_to_cure_notice_date=payload.right_to_cure_notice_date,
            sale_date=payload.sale_date,
            deficiency_notice_date=payload.deficiency_notice_date,
            lien_holder_name=payload.lien_holder_name,
            lien_recording_jurisdiction=payload.lien_recording_jurisdiction,
            title_issued_date=payload.title_issued_date,
            title_lien_notation_date=payload.title_lien_notation_date,
            # Financial
            apr=payload.apr,
            term_months=payload.term_months,
            down_payment=payload.down_payment,
            base_monthly_payment=payload.base_monthly_payment,
            financed_amount=payload.financed_amount,
            total_cost=payload.total_cost,
            fees_json=[f.model_dump() for f in payload.fees],
            add_ons_json=[a.model_dump() for a in payload.add_ons],
        )
        self.db.add(auto_details)
        self.db.flush()

        return contract, auto_details
