"""
ARKHEIA-CPS — FIA Housing Service
Layer 1: Structure all HOUSING contract entities into the database.
"""
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.common import Contract, Consumer, Counterparty, VerticalType
from app.models.housing import HousingContractDetails
from app.schemas.housing import HousingContractIn


class FIAHousingService:
    """
    FIA (Formal Identity Architecture) for HOUSING contracts.
    Parses structured JSON input and creates all lease entity records.
    """

    def __init__(self, db: Session):
        self.db = db

    def structure(self, payload: HousingContractIn) -> tuple[Contract, HousingContractDetails]:
        """
        Create Contract + Consumer + Counterparty + HousingContractDetails.
        Returns (contract, housing_details) ORM objects.
        """

        # 1. Base contract
        contract = Contract(
            type=VerticalType.HOUSING,
            jurisdiction_state=payload.jurisdiction_state.upper(),
            jurisdiction_city=payload.jurisdiction_city,
            upload_timestamp=datetime.utcnow(),
        )
        self.db.add(contract)
        self.db.flush()

        # 2. Consumer (tenant)
        consumer = Consumer(
            contract_id=contract.id,
            name=payload.consumer.name,
            email=payload.consumer.email,
            phone=payload.consumer.phone,
            reported_monthly_income=payload.consumer.reported_monthly_income,
            net_monthly_income=payload.consumer.net_monthly_income,
            household_size=payload.consumer.household_size,
        )
        self.db.add(consumer)

        # 3. Counterparty (landlord)
        counterparty = Counterparty(
            contract_id=contract.id,
            name=payload.counterparty.name,
            entity_type=payload.counterparty.entity_type,
            email=payload.counterparty.email,
            phone=payload.counterparty.phone,
            address=payload.counterparty.address,
        )
        self.db.add(counterparty)

        # 4. Housing details
        housing = HousingContractDetails(
            contract_id=contract.id,
            property_address=payload.property_address,
            unit_number=payload.unit_number,
            property_type=payload.property_type,
            bedrooms=payload.bedrooms,
            bathrooms=payload.bathrooms,
            square_footage=payload.square_footage,
            lease_start_date=payload.lease_start_date,
            lease_end_date=payload.lease_end_date,
            lease_term_months=payload.lease_term_months,
            # Financial
            base_monthly_rent=payload.base_monthly_rent,
            rent_due_day=payload.rent_due_day,
            grace_period_days=payload.grace_period_days,
            late_fee_amount=payload.late_fee_amount,
            late_fee_type=payload.late_fee_type,
            late_fee_percentage=payload.late_fee_percentage,
            rent_increase_clause_text=payload.rent_increase_clause_text,
            rent_increase_cap_percentage=payload.rent_increase_cap_percentage,
            rent_increase_frequency=payload.rent_increase_frequency,
            # Move-in
            security_deposit_amount=payload.security_deposit_amount,
            security_deposit_type=payload.security_deposit_type,
            first_month_rent_due=payload.first_month_rent_due,
            last_month_rent_due=payload.last_month_rent_due,
            application_fee_amount=payload.application_fee_amount,
            admin_fee_amount=payload.admin_fee_amount,
            other_upfront_fees_json=[f.model_dump() for f in payload.other_upfront_fees],
            # Recurring
            recurring_fees_json=[f.model_dump() for f in payload.recurring_fees],
            # Utilities
            electricity_responsibility=payload.electricity_responsibility,
            water_responsibility=payload.water_responsibility,
            gas_responsibility=payload.gas_responsibility,
            trash_responsibility=payload.trash_responsibility,
            internet_responsibility=payload.internet_responsibility,
            utility_billing_method=payload.utility_billing_method,
            utility_fee_items_json=[u.model_dump() for u in payload.utility_fee_items],
            # Maintenance
            landlord_responsible_items_json=payload.landlord_responsible_items,
            tenant_responsible_items_json=payload.tenant_responsible_items,
            emergency_response_time_hours=payload.emergency_response_time_hours,
            standard_repair_response_time_days=payload.standard_repair_response_time_days,
            maintenance_clause_text=payload.maintenance_clause_text,
            # Legal
            lease_clauses_json=[c.model_dump() for c in payload.lease_clauses],
            early_termination_penalty_amount=payload.early_termination_penalty_amount,
            early_termination_penalty_type=payload.early_termination_penalty_type,
            early_termination_months=payload.early_termination_months,
            notice_required_days_by_tenant=payload.notice_required_days_by_tenant,
            notice_required_days_by_landlord=payload.notice_required_days_by_landlord,
            automatic_renewal=payload.automatic_renewal,
            automatic_renewal_notice_days=payload.automatic_renewal_notice_days,
            termination_clause_text=payload.termination_clause_text,
            late_payment_eviction_trigger_days=payload.late_payment_eviction_trigger_days,
            eviction_notice_type=payload.eviction_notice_type,
            eviction_notice_days=payload.eviction_notice_days,
            eviction_clause_text=payload.eviction_clause_text,
            arbitration_required=payload.arbitration_required,
            dispute_venue=payload.dispute_venue,
            dispute_fee_sharing_terms=payload.dispute_fee_sharing_terms,
            dispute_resolution_clause_text=payload.dispute_resolution_clause_text,
        )
        self.db.add(housing)
        self.db.flush()

        return contract, housing
