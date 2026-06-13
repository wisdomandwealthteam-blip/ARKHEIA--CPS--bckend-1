"""
ARKHEIA-CPS — OIA-PEM Auto Service
Layer 2: Generate fairness pattern expectations for AUTO contracts.
Evaluates affordability, APR, fees, add-ons, term length, and total cost.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from app.schemas.auto import AutoContractIn
from app.schemas.common import PEMEvaluation


# ── APR benchmarks by credit band ────────────────────────────
APR_BANDS = {
    "EXCELLENT":     {"min": 0.0299, "max": 0.0599, "warn": 0.070, "fail": 0.090},
    "GOOD":          {"min": 0.0499, "max": 0.0899, "warn": 0.110, "fail": 0.140},
    "FAIR":          {"min": 0.0899, "max": 0.1499, "warn": 0.180, "fail": 0.220},
    "POOR":          {"min": 0.1499, "max": 0.2199, "warn": 0.250, "fail": 0.290},
    "DEEP_SUBPRIME": {"min": 0.1999, "max": 0.2899, "warn": 0.320, "fail": 0.360},
}

FEE_CEILINGS = {
    "DOC_FEE":    Decimal("699"),
    "DEALER_FEE": Decimal("299"),
    "TITLE":      Decimal("75"),
    "MISC":       Decimal("199"),
}

AFFORDABILITY_SAFE  = Decimal("0.15")
AFFORDABILITY_WARN  = Decimal("0.20")
ADDON_WARN_RATIO    = Decimal("0.10")
ADDON_FAIL_RATIO    = Decimal("0.20")


@dataclass
class OIAPEMAutoResult:
    evaluations:     List[PEMEvaluation] = field(default_factory=list)
    dimension_flags: dict                = field(default_factory=dict)


class OIAPEMAutoService:
    """
    OIA-PEM pattern engine for AUTO contracts.
    Generates expected fairness baselines and evaluates deviations.
    """

    def evaluate(self, payload: AutoContractIn) -> OIAPEMAutoResult:
        result = OIAPEMAutoResult()

        result.evaluations += self._eval_affordability(payload)
        result.evaluations += self._eval_apr(payload)
        result.evaluations += self._eval_fees(payload)
        result.evaluations += self._eval_addons(payload)
        result.evaluations += self._eval_total_cost(payload)
        result.evaluations += self._eval_term(payload)

        # Summarize flags for RTCSA
        result.dimension_flags = {
            "affordability_fail": any(e.pattern_family == "AFFORDABILITY" and e.status == "FAIL"
                                      for e in result.evaluations),
            "affordability_warn": any(e.pattern_family == "AFFORDABILITY" and e.status == "WARN"
                                      for e in result.evaluations),
            "apr_fail":           any(e.pattern_family == "APR" and e.status == "FAIL"
                                      for e in result.evaluations),
            "apr_warn":           any(e.pattern_family == "APR" and e.status == "WARN"
                                      for e in result.evaluations),
            "fee_fail":           any(e.pattern_family == "FEE" and e.status == "FAIL"
                                      for e in result.evaluations),
            "fee_warn":           any(e.pattern_family == "FEE" and e.status == "WARN"
                                      for e in result.evaluations),
            "addon_fail":         any(e.pattern_family == "ADDON" and e.status == "FAIL"
                                      for e in result.evaluations),
            "total_cost_fail":    any(e.pattern_family == "TOTAL_COST" and e.status == "FAIL"
                                      for e in result.evaluations),
            "term_warn":          any(e.pattern_family == "TERM" and e.status == "WARN"
                                      for e in result.evaluations),
        }

        return result

    # ── Pattern Families ─────────────────────────────────────

    def _eval_affordability(self, p: AutoContractIn) -> List[PEMEvaluation]:
        net = p.consumer.net_monthly_income or p.consumer.reported_monthly_income
        if not net or not p.base_monthly_payment:
            return [PEMEvaluation(
                pattern_family="AFFORDABILITY", pattern_key="PAYMENT_TO_INCOME",
                status="WARN", explanation="Income or payment not provided — affordability cannot be assessed."
            )]

        ratio = Decimal(str(p.base_monthly_payment)) / Decimal(str(net))

        if ratio > AFFORDABILITY_WARN:
            status = "FAIL"
            expl = (
                f"Monthly payment of ${p.base_monthly_payment:,.2f} is "
                f"{float(ratio)*100:.1f}% of net income (${net:,.2f}). "
                f"Safe limit is 15%. This contract is likely unaffordable."
            )
        elif ratio > AFFORDABILITY_SAFE:
            status = "WARN"
            expl = (
                f"Payment ({float(ratio)*100:.1f}% of income) is above the "
                f"recommended 15% threshold."
            )
        else:
            status = "OK"
            expl = f"Payment-to-income ratio of {float(ratio)*100:.1f}% is within safe range."

        return [PEMEvaluation(
            pattern_family="AFFORDABILITY", pattern_key="PAYMENT_TO_INCOME",
            expected_min=Decimal("0"), expected_max=AFFORDABILITY_SAFE,
            actual_value=ratio, status=status, explanation=expl,
        )]

    def _eval_apr(self, p: AutoContractIn) -> List[PEMEvaluation]:
        if not p.apr:
            return [PEMEvaluation(
                pattern_family="APR", pattern_key="APR_DISCLOSURE",
                status="FAIL", explanation="APR not provided. Disclosure is required by TILA and MVSFA."
            )]

        band_key = (p.consumer.credit_band or "FAIR").upper()
        bench    = APR_BANDS.get(band_key, APR_BANDS["FAIR"])
        apr      = float(p.apr)

        if apr >= bench["fail"]:
            status = "FAIL"
            expl = (
                f"APR of {apr*100:.2f}% is predatory for {band_key} credit. "
                f"Expected: {bench['min']*100:.2f}%–{bench['max']*100:.2f}%."
            )
        elif apr >= bench["warn"]:
            status = "WARN"
            expl = f"APR of {apr*100:.2f}% exceeds expected range for {band_key} credit."
        else:
            status = "OK"
            expl = f"APR of {apr*100:.2f}% is within expected range."

        return [PEMEvaluation(
            pattern_family="APR", pattern_key=f"APR_BY_BAND_{band_key}",
            expected_min=Decimal(str(bench["min"])),
            expected_max=Decimal(str(bench["max"])),
            actual_value=Decimal(str(apr)),
            status=status, explanation=expl,
        )]

    def _eval_fees(self, p: AutoContractIn) -> List[PEMEvaluation]:
        results = []
        totals: dict = {}
        for f in p.fees:
            totals[f.type] = totals.get(f.type, Decimal("0")) + f.amount

        for fee_type, total in totals.items():
            ceiling = FEE_CEILINGS.get(fee_type.upper())
            if not ceiling:
                continue
            if total > ceiling:
                results.append(PEMEvaluation(
                    pattern_family="FEE", pattern_key=f"FEE_{fee_type}",
                    expected_min=Decimal("0"), expected_max=ceiling,
                    actual_value=total, status="FAIL",
                    explanation=f"{fee_type} of ${total:,.2f} exceeds ceiling of ${ceiling:,.2f}."
                ))
            elif total > ceiling * Decimal("0.85"):
                results.append(PEMEvaluation(
                    pattern_family="FEE", pattern_key=f"FEE_{fee_type}",
                    expected_max=ceiling, actual_value=total, status="WARN",
                    explanation=f"{fee_type} of ${total:,.2f} is near the ceiling of ${ceiling:,.2f}."
                ))

        # Undisclosed fees
        hidden = [f for f in p.fees if not f.disclosed]
        if hidden:
            hidden_total = sum(f.amount for f in hidden)
            results.append(PEMEvaluation(
                pattern_family="FEE", pattern_key="UNDISCLOSED_FEES",
                actual_value=hidden_total, status="FAIL",
                explanation=f"{len(hidden)} undisclosed fee(s) totaling ${hidden_total:,.2f} detected."
            ))

        return results

    def _eval_addons(self, p: AutoContractIn) -> List[PEMEvaluation]:
        if not p.add_ons or not p.financed_amount:
            return []

        total_addon = sum(a.price for a in p.add_ons)
        ratio       = total_addon / p.financed_amount

        if ratio > ADDON_FAIL_RATIO:
            status = "FAIL"
            expl = f"Add-ons total ${total_addon:,.2f} ({float(ratio)*100:.1f}% of loan) — excessive."
        elif ratio > ADDON_WARN_RATIO:
            status = "WARN"
            expl = f"Add-ons total ${total_addon:,.2f} ({float(ratio)*100:.1f}% of loan) — elevated."
        else:
            status = "OK"
            expl = f"Add-on total ${total_addon:,.2f} is proportionate."

        evals = [PEMEvaluation(
            pattern_family="ADDON", pattern_key="ADDON_TOTAL_RATIO",
            expected_max=ADDON_WARN_RATIO, actual_value=ratio,
            status=status, explanation=expl,
        )]

        forced = [a for a in p.add_ons if not a.optional]
        if forced:
            forced_total = sum(a.price for a in forced)
            evals.append(PEMEvaluation(
                pattern_family="ADDON", pattern_key="FORCED_ADDONS",
                actual_value=forced_total, status="FAIL",
                explanation=f"{len(forced)} add-on(s) totaling ${forced_total:,.2f} presented as mandatory."
            ))

        return evals

    def _eval_total_cost(self, p: AutoContractIn) -> List[PEMEvaluation]:
        if not (p.base_monthly_payment and p.term_months and p.total_cost):
            return []

        expected    = p.base_monthly_payment * p.term_months + p.down_payment
        variance    = abs(expected - p.total_cost)
        status      = "FAIL" if variance > 50 else ("WARN" if variance > 10 else "OK")
        explanation = (
            f"Computed total ${expected:,.2f} vs stated ${p.total_cost:,.2f} "
            f"— variance of ${variance:,.2f}."
            if status != "OK" else "Total cost matches payment schedule."
        )

        return [PEMEvaluation(
            pattern_family="TOTAL_COST", pattern_key="TOTAL_COST_ACCURACY",
            expected_min=expected - 10, expected_max=expected + 10,
            actual_value=p.total_cost, status=status, explanation=explanation,
        )]

    def _eval_term(self, p: AutoContractIn) -> List[PEMEvaluation]:
        if not p.term_months:
            return []
        if p.term_months > 84:
            return [PEMEvaluation(
                pattern_family="TERM", pattern_key="TERM_LENGTH",
                expected_max=Decimal("84"), actual_value=Decimal(str(p.term_months)),
                status="WARN",
                explanation=f"Loan term of {p.term_months} months exceeds 84-month threshold. Increases negative equity risk."
            )]
        return [PEMEvaluation(
            pattern_family="TERM", pattern_key="TERM_LENGTH",
            actual_value=Decimal(str(p.term_months)), status="OK",
            explanation=f"Term of {p.term_months} months is within acceptable range."
        )]
