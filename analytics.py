"""
Workforce analytics — the "hard" stuff, made simple and explainable.

Enterprise HR platforms sell attrition prediction and pay-equity analysis as
premium, black-box features. Here we implement transparent versions:

  - predict_attrition_risk: a weighted, EXPLAINABLE scoring model. No black box —
    it tells you exactly which factors drove the score. (Explainability is
    exactly what HR/legal teams demand from "AI" in hiring/retention.)

  - analyze_pay_equity: compares pay within the same role to surface gaps,
    including a gender pay-gap check — a real US compliance concern.

Pure Python, no ML libraries, so it runs anywhere.
"""

from statistics import median
from sample_data import EMPLOYEES


# ---------------------------------------------------------------------------
# ATTRITION / FLIGHT-RISK PREDICTION
# ---------------------------------------------------------------------------
# Each rule adds "risk points" and records WHY. This is the whole model —
# readable, auditable, and easy to tune. Real systems bury this in a black box.
def _attrition_factors(emp: dict) -> list[tuple[str, int]]:
    factors: list[tuple[str, int]] = []

    engagement = emp["engagement_score"]
    if engagement <= 2:
        factors.append((f"Low engagement score ({engagement}/5)", 35))
    elif engagement == 3:
        factors.append(("Neutral engagement score (3/5)", 10))

    since_raise = emp["months_since_last_raise"]
    if since_raise >= 18:
        factors.append((f"No raise in {since_raise} months", 25))
    elif since_raise >= 12:
        factors.append((f"No raise in {since_raise} months", 12))

    leave_taken = emp["leave_days_taken_last_year"]
    if leave_taken <= 3:
        factors.append((f"Almost no leave taken ({leave_taken} days) — burnout signal", 20))

    tenure = emp["tenure_months"]
    if tenure < 18:
        factors.append((f"Short tenure ({tenure} months) — early-attrition window", 10))

    return factors


def predict_attrition_risk(employee_id: str) -> dict:
    """Return an explainable attrition-risk assessment for one employee."""
    emp = EMPLOYEES.get(employee_id)
    if not emp:
        return {"error": f"No employee found with ID {employee_id}."}

    factors = _attrition_factors(emp)
    score = min(100, sum(points for _, points in factors))
    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "employee": emp["name"],
        "employee_id": employee_id,
        "risk_score": score,
        "risk_level": level,
        "top_factors": [f"{desc} (+{pts})" for desc, pts in
                        sorted(factors, key=lambda x: -x[1])] or ["No notable risk factors"],
    }


# ---------------------------------------------------------------------------
# PAY-EQUITY ANALYSIS
# ---------------------------------------------------------------------------
def analyze_pay_equity(role: str = "") -> dict:
    """Analyze pay fairness within a role (or all roles if none given).

    Flags anyone paid notably below the role median, and reports the
    gender pay gap within each role.
    """
    # Group employees by role.
    by_role: dict[str, list[dict]] = {}
    for emp in EMPLOYEES.values():
        if role and emp["role"].lower() != role.lower():
            continue
        by_role.setdefault(emp["role"], []).append(emp)

    if not by_role:
        return {"error": f"No employees found for role '{role}'."}

    findings = []
    for role_name, people in by_role.items():
        if len(people) < 2:
            continue  # need at least 2 to compare
        salaries = [p["salary_usd"] for p in people]
        role_median = median(salaries)

        # Flag anyone >10% below the role median.
        below = []
        for p in people:
            gap_pct = (role_median - p["salary_usd"]) / role_median * 100
            if gap_pct >= 10:
                below.append(
                    f"{p['name']} earns ${p['salary_usd']:,} "
                    f"({gap_pct:.0f}% below role median ${int(role_median):,})"
                )

        # Gender pay gap within the role.
        male = [p["salary_usd"] for p in people if p["gender"] == "M"]
        female = [p["salary_usd"] for p in people if p["gender"] == "F"]
        gender_note = ""
        if male and female:
            gap = (median(male) - median(female)) / median(male) * 100
            if abs(gap) >= 5:
                higher = "men" if gap > 0 else "women"
                gender_note = (
                    f"Gender pay gap: median pay for {higher} is "
                    f"{abs(gap):.0f}% higher in this role."
                )

        findings.append({
            "role": role_name,
            "employees": len(people),
            "median_salary_usd": int(role_median),
            "below_median_flags": below or ["None — pay looks equitable."],
            "gender_gap": gender_note or "No significant gender pay gap detected.",
        })

    return {"analysis": findings}
