"""
Sample HR data for the demo.

In a real deployment this would come from a database (Darwinbox uses MongoDB).
For our demo, a plain Python dictionary is enough to prove the idea works.
Everything here is fake, made-up data for a pretend company called "Acme Corp".

(US state payroll/compliance rules now live in compliance_data.py.)
"""

# --- Employees ---------------------------------------------------------------
EMPLOYEES = {
    "E1001": {
        "name": "Priya Sharma",
        "work_state": "TX",          # Texas
        "leave_balance_days": 12,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
        "manager_email": "ravi.kumar@example.com",
        "onboarding_complete": True,
    },
    "E1002": {
        "name": "John Miller",
        "work_state": "CA",          # California
        "leave_balance_days": 4,
        "manager": "Sara Lopez",
        "manager_slack": "@sara",
        "manager_email": "sara.lopez@example.com",
        "onboarding_complete": False,
    },
    "E1003": {
        "name": "Wei Chen",
        "work_state": "NY",          # New York
        "leave_balance_days": 18,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
        "manager_email": "ravi.kumar@example.com",
        "onboarding_complete": False,
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
