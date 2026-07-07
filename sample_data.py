"""
Sample HR data for the demo.

In a real deployment this would come from a database (Darwinbox uses MongoDB).
For our demo, a plain Python dictionary is enough to prove the idea works.
Everything here is fake, made-up data for a pretend company called "Acme Corp".

(US state payroll/compliance rules live in compliance_data.py.)
"""

# --- Employees ---------------------------------------------------------------
# Extra fields (department, salary, tenure, engagement, etc.) power the
# advanced analytics tools: attrition risk and pay-equity analysis.
EMPLOYEES = {
    "E1001": {
        "name": "Priya Sharma",
        "department": "Engineering",
        "role": "Software Engineer",
        "work_state": "TX",
        "gender": "F",
        "salary_usd": 118000,
        "tenure_months": 30,
        "engagement_score": 4,          # 1 (low) .. 5 (high)
        "months_since_last_raise": 8,
        "leave_days_taken_last_year": 14,
        "leave_balance_days": 12,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
        "manager_email": "ravi.kumar@example.com",
        "onboarding_complete": True,
    },
    "E1002": {
        "name": "John Miller",
        "department": "Engineering",
        "role": "Software Engineer",
        "work_state": "CA",
        "gender": "M",
        "salary_usd": 135000,
        "tenure_months": 42,
        "engagement_score": 2,
        "months_since_last_raise": 22,
        "leave_days_taken_last_year": 3,
        "leave_balance_days": 4,
        "manager": "Sara Lopez",
        "manager_slack": "@sara",
        "manager_email": "sara.lopez@example.com",
        "onboarding_complete": False,
    },
    "E1003": {
        "name": "Wei Chen",
        "department": "Engineering",
        "role": "Senior Software Engineer",
        "work_state": "NY",
        "gender": "M",
        "salary_usd": 158000,
        "tenure_months": 60,
        "engagement_score": 5,
        "months_since_last_raise": 5,
        "leave_days_taken_last_year": 16,
        "leave_balance_days": 18,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
        "manager_email": "ravi.kumar@example.com",
        "onboarding_complete": False,
    },
    "E1004": {
        "name": "Aisha Khan",
        "department": "Engineering",
        "role": "Senior Software Engineer",
        "work_state": "WA",
        "gender": "F",
        "salary_usd": 139000,      # notably below the male peer at same role
        "tenure_months": 55,
        "engagement_score": 3,
        "months_since_last_raise": 19,
        "leave_days_taken_last_year": 9,
        "leave_balance_days": 10,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
        "manager_email": "ravi.kumar@example.com",
        "onboarding_complete": True,
    },
    "E1005": {
        "name": "Diego Torres",
        "department": "Sales",
        "role": "Account Executive",
        "work_state": "FL",
        "gender": "M",
        "salary_usd": 92000,
        "tenure_months": 14,
        "engagement_score": 1,
        "months_since_last_raise": 14,
        "leave_days_taken_last_year": 2,
        "leave_balance_days": 6,
        "manager": "Sara Lopez",
        "manager_slack": "@sara",
        "manager_email": "sara.lopez@example.com",
        "onboarding_complete": True,
    },
}

# --- A simple onboarding checklist a new hire must complete -----------------
ONBOARDING_CHECKLIST = [
    "Sign offer letter",
    "Submit Form I-9 (employment eligibility)",
    "Complete W-4 tax withholding form",
    "Enroll in health benefits",
    "Set up direct deposit",
    "Complete IT security training",
]
