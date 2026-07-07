"""
US payroll & employment compliance rules.

This is the "brain" behind the compliance tools. It targets Darwinbox's known
weak spot vs. Rippling: deep US payroll/compliance coverage.

IMPORTANT — this data is SIMPLIFIED and ILLUSTRATIVE (values roughly as of 2026).
Real payroll compliance changes constantly and varies by city/county. In a real
product these numbers would come from a maintained legal database. The point of
this project is to show the *structure* and *logic* an HR agent needs.
"""

# ---------------------------------------------------------------------------
# FEDERAL rules — apply to every US employee regardless of state
# ---------------------------------------------------------------------------
FEDERAL_RULES = {
    "minimum_wage_usd": 7.25,          # Federal minimum wage (FLSA)
    "overtime_multiplier": 1.5,         # Time-and-a-half...
    "overtime_threshold_hours": 40,     # ...for hours worked over 40/week (FLSA)
    "overtime_exempt_salary_usd": 43888,  # Approx. salary threshold for exemption
    "i9_required": True,                # Every US hire must complete Form I-9
    "everify_required_federally": False,  # E-Verify is federal-contractor / state-driven
}

# ---------------------------------------------------------------------------
# STATE rules — a representative set of the biggest employment states.
# Fields:
#   income_tax           : does the state levy personal income tax?
#   min_wage_usd         : state minimum wage (use max(state, federal) in practice)
#   withholding_form     : the state tax withholding form a new hire signs
#   everify_mandatory    : is E-Verify required for employers in this state?
#   notes                : anything special an HR/payroll team must know
# ---------------------------------------------------------------------------
STATE_RULES = {
    "AL": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "A-4",     "everify_mandatory": True,  "notes": "E-Verify mandatory for most employers."},
    "AZ": {"income_tax": True,  "min_wage_usd": 14.35, "withholding_form": "A-4",     "everify_mandatory": True,  "notes": "E-Verify mandatory statewide."},
    "CA": {"income_tax": True,  "min_wage_usd": 16.00, "withholding_form": "DE 4",    "everify_mandatory": False, "notes": "Mandatory SDI deduction; many cities set higher local minimum wage."},
    "CO": {"income_tax": True,  "min_wage_usd": 14.42, "withholding_form": "DR 0004",  "everify_mandatory": False, "notes": "Daily overtime after 12 hours worked."},
    "FL": {"income_tax": False, "min_wage_usd": 13.00, "withholding_form": None,       "everify_mandatory": True,  "notes": "No state income tax. E-Verify required for private employers with 25+ staff."},
    "GA": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "G-4",     "everify_mandatory": True,  "notes": "E-Verify required for employers with 10+ employees."},
    "IL": {"income_tax": True,  "min_wage_usd": 14.00, "withholding_form": "IL-W-4",  "everify_mandatory": False, "notes": "Flat state income tax rate."},
    "MA": {"income_tax": True,  "min_wage_usd": 15.00, "withholding_form": "M-4",     "everify_mandatory": False, "notes": "Daily/Sunday premium pay rules for some sectors."},
    "NC": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "NC-4",    "everify_mandatory": True,  "notes": "E-Verify required for employers with 25+ employees."},
    "NV": {"income_tax": False, "min_wage_usd": 12.00, "withholding_form": None,       "everify_mandatory": False, "notes": "No state income tax. Daily overtime after 8 hours for lower-wage workers."},
    "NY": {"income_tax": True,  "min_wage_usd": 15.00, "withholding_form": "IT-2104",  "everify_mandatory": False, "notes": "NYC and Long Island have higher local minimum wage; NYC residents owe city tax."},
    "OH": {"income_tax": True,  "min_wage_usd": 10.45, "withholding_form": "IT 4",    "everify_mandatory": False, "notes": "Some municipalities levy local income tax."},
    "PA": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "REV-419",  "everify_mandatory": False, "notes": "Flat state income tax; many localities add local Earned Income Tax."},
    "TX": {"income_tax": False, "min_wage_usd": 7.25,  "withholding_form": None,       "everify_mandatory": False, "notes": "No state income tax. Follows federal minimum wage."},
    "WA": {"income_tax": False, "min_wage_usd": 16.28, "withholding_form": None,       "everify_mandatory": False, "notes": "No state income tax but has Paid Family & Medical Leave payroll deduction."},
}

SUPPORTED_STATES = sorted(STATE_RULES.keys())
