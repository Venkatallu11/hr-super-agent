"""
US payroll & employment compliance rules — all 50 states + DC.

This is the "brain" behind the compliance tools. It targets Darwinbox's known
weak spot vs. Rippling: deep US payroll/compliance coverage.

IMPORTANT — this data is SIMPLIFIED and ILLUSTRATIVE (values roughly as of 2026).
Real payroll compliance changes constantly and varies by city/county. In a real
product these numbers would come from a maintained legal database. The point of
this project is to show the *structure*, *national coverage*, and *logic* an HR
agent needs — not to be a source of legal truth.

Field meanings per state:
  income_tax        : does the state levy personal income tax on wages?
  min_wage_usd      : state minimum wage (use max(state, federal) in practice)
  withholding_form  : the state tax withholding certificate a new hire signs
                      (None where there is no state wage income tax)
  everify_mandatory : is E-Verify broadly required for private employers?
  notes             : anything special an HR/payroll team must know
"""

# ---------------------------------------------------------------------------
# FEDERAL rules — apply to every US employee regardless of state
# ---------------------------------------------------------------------------
FEDERAL_RULES = {
    "minimum_wage_usd": 7.25,           # Federal minimum wage (FLSA)
    "overtime_multiplier": 1.5,          # Time-and-a-half...
    "overtime_threshold_hours": 40,      # ...for hours worked over 40/week (FLSA)
    "overtime_exempt_salary_usd": 43888,  # Approx. salary threshold for exemption
    "i9_required": True,                 # Every US hire must complete Form I-9
    "everify_required_federally": False,  # E-Verify is federal-contractor / state-driven
}

# ---------------------------------------------------------------------------
# STATE rules — all 50 states + DC
# ---------------------------------------------------------------------------
_STATE = "state withholding certificate"  # generic label where form code varies

STATE_RULES = {
    "AL": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "A-4",     "everify_mandatory": True,  "notes": "E-Verify mandatory for all employers."},
    "AK": {"income_tax": False, "min_wage_usd": 11.73, "withholding_form": None,      "everify_mandatory": False, "notes": "No state income tax."},
    "AZ": {"income_tax": True,  "min_wage_usd": 14.35, "withholding_form": "A-4",     "everify_mandatory": True,  "notes": "E-Verify mandatory statewide."},
    "AR": {"income_tax": True,  "min_wage_usd": 11.00, "withholding_form": "AR4EC",   "everify_mandatory": False, "notes": "E-Verify required for public employers/contractors."},
    "CA": {"income_tax": True,  "min_wage_usd": 16.00, "withholding_form": "DE 4",    "everify_mandatory": False, "notes": "Mandatory SDI deduction; many cities set higher local minimum wage; daily overtime after 8h."},
    "CO": {"income_tax": True,  "min_wage_usd": 14.42, "withholding_form": "DR 0004", "everify_mandatory": False, "notes": "Daily overtime after 12 hours worked."},
    "CT": {"income_tax": True,  "min_wage_usd": 15.69, "withholding_form": "CT-W4",   "everify_mandatory": False, "notes": "Minimum wage indexed to inflation."},
    "DE": {"income_tax": True,  "min_wage_usd": 13.25, "withholding_form": _STATE,    "everify_mandatory": False, "notes": "Scheduled minimum wage increases."},
    "DC": {"income_tax": True,  "min_wage_usd": 17.50, "withholding_form": "D-4",     "everify_mandatory": False, "notes": "Highest minimum wage in the country; indexed annually."},
    "FL": {"income_tax": False, "min_wage_usd": 13.00, "withholding_form": None,      "everify_mandatory": True,  "notes": "No state income tax. E-Verify required for private employers with 25+ staff; rising to $15 by 2026."},
    "GA": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "G-4",     "everify_mandatory": True,  "notes": "E-Verify required for employers with 10+ employees."},
    "HI": {"income_tax": True,  "min_wage_usd": 14.00, "withholding_form": "HW-4",    "everify_mandatory": False, "notes": "Scheduled to reach $18 by 2028."},
    "ID": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "ID W-4",  "everify_mandatory": False, "notes": "Follows federal minimum wage."},
    "IL": {"income_tax": True,  "min_wage_usd": 14.00, "withholding_form": "IL-W-4",  "everify_mandatory": False, "notes": "Flat state income tax rate; Chicago sets a higher local minimum wage."},
    "IN": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "WH-4",    "everify_mandatory": False, "notes": "County income taxes also apply."},
    "IA": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "IA W-4",  "everify_mandatory": False, "notes": "Follows federal minimum wage."},
    "KS": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "K-4",     "everify_mandatory": False, "notes": "Follows federal minimum wage."},
    "KY": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "K-4",     "everify_mandatory": False, "notes": "Many localities levy local occupational taxes."},
    "LA": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "L-4",     "everify_mandatory": False, "notes": "No state minimum wage law; federal applies."},
    "ME": {"income_tax": True,  "min_wage_usd": 14.15, "withholding_form": "W-4ME",   "everify_mandatory": False, "notes": "Minimum wage indexed to inflation."},
    "MD": {"income_tax": True,  "min_wage_usd": 15.00, "withholding_form": "MW507",   "everify_mandatory": False, "notes": "County income taxes also apply."},
    "MA": {"income_tax": True,  "min_wage_usd": 15.00, "withholding_form": "M-4",     "everify_mandatory": False, "notes": "Daily/Sunday premium pay rules in some sectors."},
    "MI": {"income_tax": True,  "min_wage_usd": 10.33, "withholding_form": "MI-W4",   "everify_mandatory": False, "notes": "Some cities levy local income tax."},
    "MN": {"income_tax": True,  "min_wage_usd": 10.85, "withholding_form": "W-4MN",   "everify_mandatory": False, "notes": "Minneapolis/St. Paul set higher local minimum wage."},
    "MS": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "89-350",  "everify_mandatory": True,  "notes": "E-Verify mandatory for all employers."},
    "MO": {"income_tax": True,  "min_wage_usd": 12.30, "withholding_form": "MO W-4",  "everify_mandatory": False, "notes": "Minimum wage indexed to inflation."},
    "MT": {"income_tax": True,  "min_wage_usd": 10.30, "withholding_form": "MW-4",    "everify_mandatory": False, "notes": "Minimum wage indexed to inflation."},
    "NE": {"income_tax": True,  "min_wage_usd": 12.00, "withholding_form": "W-4N",    "everify_mandatory": False, "notes": "Scheduled increases toward $15."},
    "NV": {"income_tax": False, "min_wage_usd": 12.00, "withholding_form": None,      "everify_mandatory": False, "notes": "No state income tax. Daily overtime after 8h for lower-wage workers."},
    "NH": {"income_tax": False, "min_wage_usd": 7.25,  "withholding_form": None,      "everify_mandatory": False, "notes": "No tax on earned wages. Follows federal minimum wage."},
    "NJ": {"income_tax": True,  "min_wage_usd": 15.13, "withholding_form": "NJ-W4",   "everify_mandatory": False, "notes": "Minimum wage indexed to inflation."},
    "NM": {"income_tax": True,  "min_wage_usd": 12.00, "withholding_form": _STATE,    "everify_mandatory": False, "notes": "Some cities/counties set higher local minimum wage."},
    "NY": {"income_tax": True,  "min_wage_usd": 15.00, "withholding_form": "IT-2104", "everify_mandatory": False, "notes": "NYC/Long Island have higher local minimum wage; NYC residents owe city tax."},
    "NC": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "NC-4",    "everify_mandatory": True,  "notes": "E-Verify required for employers with 25+ employees."},
    "ND": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": _STATE,    "everify_mandatory": False, "notes": "Follows federal minimum wage."},
    "OH": {"income_tax": True,  "min_wage_usd": 10.45, "withholding_form": "IT 4",    "everify_mandatory": False, "notes": "Some municipalities levy local income tax."},
    "OK": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "OK-W-4",  "everify_mandatory": False, "notes": "Follows federal minimum wage."},
    "OR": {"income_tax": True,  "min_wage_usd": 14.70, "withholding_form": "OR-W-4",  "everify_mandatory": False, "notes": "Tiered minimum wage by region (Portland metro higher)."},
    "PA": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "REV-419", "everify_mandatory": False, "notes": "Flat state income tax; many localities add local Earned Income Tax."},
    "RI": {"income_tax": True,  "min_wage_usd": 14.00, "withholding_form": "RI W-4",  "everify_mandatory": False, "notes": "Scheduled increases toward $15."},
    "SC": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "SC W-4",  "everify_mandatory": True,  "notes": "E-Verify mandatory for all employers."},
    "SD": {"income_tax": False, "min_wage_usd": 11.20, "withholding_form": None,      "everify_mandatory": False, "notes": "No state income tax. Minimum wage indexed to inflation."},
    "TN": {"income_tax": False, "min_wage_usd": 7.25,  "withholding_form": None,      "everify_mandatory": True,  "notes": "No state income tax. E-Verify required for employers with 35+ employees."},
    "TX": {"income_tax": False, "min_wage_usd": 7.25,  "withholding_form": None,      "everify_mandatory": False, "notes": "No state income tax. Follows federal minimum wage."},
    "UT": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": _STATE,    "everify_mandatory": True,  "notes": "E-Verify required for employers with 15+ employees."},
    "VT": {"income_tax": True,  "min_wage_usd": 13.67, "withholding_form": "W-4VT",   "everify_mandatory": False, "notes": "Minimum wage indexed to inflation."},
    "VA": {"income_tax": True,  "min_wage_usd": 12.00, "withholding_form": "VA-4",    "everify_mandatory": False, "notes": "Scheduled increases toward $15."},
    "WA": {"income_tax": False, "min_wage_usd": 16.28, "withholding_form": None,      "everify_mandatory": False, "notes": "No wage income tax but has Paid Family & Medical Leave payroll deduction; Seattle higher local minimum wage."},
    "WV": {"income_tax": True,  "min_wage_usd": 8.75,  "withholding_form": "WV/IT-104", "everify_mandatory": False, "notes": "State minimum wage above federal."},
    "WI": {"income_tax": True,  "min_wage_usd": 7.25,  "withholding_form": "WT-4",    "everify_mandatory": False, "notes": "Follows federal minimum wage."},
    "WY": {"income_tax": False, "min_wage_usd": 7.25,  "withholding_form": None,      "everify_mandatory": False, "notes": "No state income tax. Follows federal minimum wage."},
}

SUPPORTED_STATES = sorted(STATE_RULES.keys())
