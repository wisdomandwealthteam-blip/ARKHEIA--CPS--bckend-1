"""
ARKHEIA-CPS — Explanation Generator
Produces plain-language, consumer-first explanations for every violation type.
Tone: protective, empowering, non-technical.
"""
from __future__ import annotations
from decimal import Decimal
from typing import List, Optional

from app.schemas.common import Alert


# ── AUTO explanations ─────────────────────────────────────────

def generate_auto_explanations(
    alerts: List[Alert],
    perfection_days: Optional[int],
    illegal_patterns: List[str],
) -> List[str]:
    explanations = []

    # Perfection timing narrative
    if perfection_days is not None:
        if perfection_days > 90:
            explanations.append(
                f"The lender perfected the lien {perfection_days} days after purchase. "
                f"Typical perfection occurs within 10–30 days. This severe delay may affect "
                f"the legality of any repossession or enforcement action taken against you. "
                f"Consult an attorney before making any payments or surrendering the vehicle."
            )
        elif perfection_days > 60:
            explanations.append(
                f"The lender perfected the lien {perfection_days} days after purchase — "
                f"a high deviation from the expected 10–30 day window. This may create "
                f"questions about the enforceability of the lender's security interest."
            )
        elif perfection_days > 30:
            explanations.append(
                f"The lien was perfected {perfection_days} days after purchase. "
                f"This is slightly above the typical 10–30 day window. "
                f"Request documentation confirming the perfection date from your lender."
            )

    # Illegal pattern narratives
    for pattern in illegal_patterns:
        if "PERF_AFTER_REPO" in pattern:
            explanations.append(
                "CRITICAL: The lender repossessed your vehicle before their lien was legally "
                "perfected. This means they had no legal right to take the vehicle. "
                "You may be entitled to the return of the vehicle and damages. "
                "Contact a consumer protection attorney immediately."
            )
        if "REPO_NO_NOTICE" in pattern:
            explanations.append(
                "CRITICAL: Your vehicle was repossessed before you received a notice of "
                "default. In most states, lenders are required to notify you before taking "
                "action. This repossession may be unlawful. Do not pay any deficiency "
                "balance until you speak with an attorney."
            )
        if "REPO_BEFORE_CURE" in pattern:
            explanations.append(
                "CRITICAL: The lender did not give you enough time to cure the default "
                "before repossessing the vehicle. Georgia law requires lenders to give you "
                "a right-to-cure notice and adequate time to catch up on payments. "
                "This repossession may violate O.C.G.A. § 10-1-36."
            )
        if "REPO_CURE_TOO_SOON" in pattern:
            explanations.append(
                "The lender did not wait the legally required number of days after sending "
                "the right-to-cure notice before repossessing the vehicle. "
                "The cure period was not fully honored."
            )
        if "PERF_SAME_DAY" in pattern:
            explanations.append(
                "The lender perfected the lien and repossessed the vehicle on the same day. "
                "This is a predatory pattern that suggests the repossession was planned "
                "before the lien was legally established. Seek legal counsel."
            )

    # Alert-based narratives (non-perfection)
    for alert in alerts:
        code = alert.code
        if "AFFORDABILITY" in code or "PAYMENT_TO_INCOME" in code:
            explanations.append(
                "Your monthly payment appears to exceed what is typically considered affordable "
                "based on your income. Financial experts recommend that car payments stay "
                "below 15% of your take-home pay. At this level, you may have difficulty "
                "covering other essential expenses."
            )
        elif "APR" in code and "PREDATORY" not in code:
            explanations.append(
                f"The interest rate on this loan is above the typical range for someone with "
                f"your credit profile. A high APR means you will pay significantly more "
                f"over the life of the loan. Shop around at credit unions and banks — "
                f"you may qualify for a better rate."
            )
        elif "UNDISCLOSED" in code:
            explanations.append(
                "One or more fees on this contract were not clearly disclosed to you before "
                "signing. Georgia law and federal Truth-in-Lending rules require that all "
                "fees be clearly itemized. Request a full fee disclosure in writing."
            )
        elif "FORCED" in code or "ADDON" in code:
            explanations.append(
                "One or more add-on products (such as extended warranties or GAP insurance) "
                "appear to have been presented as required. These products are always optional "
                "under Georgia law. You have the right to decline them."
            )
        elif "TOTAL_COST" in code:
            explanations.append(
                "The total cost stated in the contract does not match what the payment "
                "schedule would add up to. This discrepancy may indicate hidden charges "
                "or a math error in your contract. Request a detailed payoff schedule."
            )

    # Deduplicate
    seen = set()
    unique = []
    for e in explanations:
        key = e[:60]
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique


# ── HOUSING explanations ──────────────────────────────────────

def generate_housing_explanations(
    alerts: List[Alert],
    payload,
    illegal_clauses: List[str],
    total_movein: Decimal,
) -> List[str]:
    explanations = []
    rent = payload.base_monthly_rent

    # Move-in cost narrative
    months_equiv = float(total_movein / rent) if rent > 0 else 0
    if months_equiv > 3.0:
        explanations.append(
            f"Your total move-in cost is ${total_movein:,.2f} — that's {months_equiv:.1f} "
            f"months of rent upfront. Amounts above 3× monthly rent are considered predatory "
            f"in most jurisdictions and may violate state security deposit limits."
        )
    elif months_equiv > 2.5:
        explanations.append(
            f"Your total move-in cost of ${total_movein:,.2f} ({months_equiv:.1f}× rent) "
            f"is above the typical 2× guideline. Ask the landlord to itemize every charge."
        )

    # Illegal clause narratives
    if illegal_clauses:
        explanations.append(
            f"This lease contains {len(illegal_clauses)} clause(s) that may be illegal "
            f"or unenforceable under tenant protection law: "
            f"{'; '.join(f'\"{c}\"' for c in illegal_clauses[:3])}. "
            f"Clauses that waive your legal rights, allow entry without notice, or disclaim "
            f"habitability obligations may not be enforceable even if you signed the lease."
        )

    # Alert-based narratives
    for alert in alerts:
        code = alert.code
        if "RENT_TO_INCOME" in code:
            ratio_pct = float(rent / (payload.consumer.net_monthly_income or payload.consumer.reported_monthly_income or 1)) * 100
            explanations.append(
                f"Your rent of ${rent:,.2f}/month is approximately {ratio_pct:.0f}% of your "
                f"take-home income. Housing experts recommend spending no more than 30% of "
                f"net income on rent. At this level, you may face financial hardship."
            )
        elif "APPLICATION_FEE" in code:
            explanations.append(
                f"The application fee of ${payload.application_fee_amount:,.2f} exceeds "
                f"typical limits ($25–$75). High application fees can be a predatory tactic, "
                f"especially if the landlord collects fees from many applicants with no "
                f"intention of renting to all of them."
            )
        elif "ADMIN_FEE" in code:
            explanations.append(
                f"The administrative fee of ${payload.admin_fee_amount:,.2f} is above "
                f"the typical range ($0–$150). Ask the landlord to explain exactly what "
                f"service this fee covers."
            )
        elif "SECURITY_DEPOSIT" in code:
            explanations.append(
                f"The security deposit of ${payload.security_deposit_amount:,.2f} may "
                f"exceed the legal limit in your state. Many states cap security deposits "
                f"at 1–2 months' rent. Check your state's tenant protection laws."
            )
        elif "RENT_INCREASE" in code:
            explanations.append(
                "The rent increase clause in this lease allows for above-average rent hikes. "
                "High rent increase caps can make your housing costs unpredictable over time. "
                "If you sign a multi-year lease, negotiate a lower cap in writing."
            )
        elif "LATE_FEE" in code:
            explanations.append(
                f"The late fee of ${payload.late_fee_amount:,.2f} is above the recommended "
                f"maximum. Excessive late fees can quickly compound if you miss a payment, "
                f"making it harder to catch up."
            )
        elif "GRACE_PERIOD" in code:
            explanations.append(
                "This lease has no grace period or a very short one before late fees apply. "
                "A grace period of at least 3–5 days protects you if rent processing is delayed."
            )
        elif "AUTO_RENEWAL" in code:
            explanations.append(
                "This lease automatically renews without adequate advance notice. "
                "If you don't plan to renew, you could be locked into another term. "
                "Mark your calendar at least 60 days before the lease ends."
            )
        elif "EARLY_TERMINATION" in code:
            explanations.append(
                "The early termination penalty in this lease is high. If you need to "
                "leave before the lease ends for any reason, you could owe several months' "
                "rent. Negotiate this clause before signing."
            )
        elif "EVICTION" in code:
            explanations.append(
                "The eviction clause in this lease may allow the landlord to begin eviction "
                "proceedings faster than state law normally permits. Know your rights: "
                "most states require proper notice and a court hearing before you can be "
                "legally removed."
            )
        elif "ILLEGAL_CLAUSE" in code:
            explanations.append(
                "One or more clauses in this lease may be illegal and unenforceable. "
                "Signing a lease does not mean you waive rights that are protected by law. "
                "Consult a tenant rights organization or attorney before signing."
            )

    # Deduplicate
    seen = set()
    unique = []
    for e in explanations:
        key = e[:60]
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique
