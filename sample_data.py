"""
Sample HR data for the demo.

In a real deployment this would come from a database (Darwinbox uses MongoDB).
For our demo, a plain Python dictionary is enough to prove the idea works.
Everything here is fake, made-up data for a pretend company called "Acme Corp".
"""

# --- Employees and their leave balances -------------------------------------
EMPLOYEES = {
    "E1001": {
        "name": "Priya Sharma",
        "work_state": "TX",          # Texas
        "leave_balance_days": 12,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
        "onboarding_complete": True,
    },
    "E1002": {
        "name": "John Miller",
        "work_state": "CA",          # California
        "leave_balance_days": 4,
        "manager": "Sara Lopez",
        "manager_slack": "@sara",
        "onboarding_complete": False,
    },
    "E1003": {
        "name": "Wei Chen",
        "work_state": "NY",          # New York
        "leave_balance_days": 18,
        "manager": "Ravi Kumar",
        "manager_slack": "@ravi",
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

# --- US state payroll rules (simplified for the demo) -----------------------
# Real US payroll compliance is huge; this is a small, honest slice to show
# the idea. It targets Darwinbox's known weak spot: deep US payroll/compliance.
US_STATE_TAX_RULES = {
    "TX": {
        "state_income_tax": False,
        "note": "Texas has NO state income tax.",
        "extra_forms": [],
    },
    "CA": {
        "state_income_tax": True,
        "note": "California has state income tax and mandatory SDI (disability) deductions.",
        "extra_forms": ["DE 4 (CA state withholding)"],
    },
    "NY": {
        "state_income_tax": True,
        "note": "New York has state income tax; NYC residents also owe city tax.",
        "extra_forms": ["IT-2104 (NY state withholding)"],
    },
}
