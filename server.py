"""
HR Super Agent — MCP Server
===========================

This is an MCP (Model Context Protocol) server that exposes HR "tools".
Any MCP-compatible AI agent (Claude Desktop, or Darwinbox's Super Agent)
can connect to this server and call these tools to get real work done.

Each function decorated with @mcp.tool() becomes a tool the AI can use.
That is the whole trick: an MCP tool is just a normal Python function with a
label on it, plus a clear description so the AI knows when to use it.

Run it with:   python server.py
"""

from mcp.server.fastmcp import FastMCP

from sample_data import EMPLOYEES, ONBOARDING_CHECKLIST
from compliance_data import FEDERAL_RULES, STATE_RULES, SUPPORTED_STATES
from integrations import deliver

# Create the server. The name shows up in the AI client's tool list.
mcp = FastMCP("HR Super Agent")


# ===========================================================================
# HR DATA TOOLS
# ===========================================================================
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Get how many paid vacation/leave days an employee has left.

    Args:
        employee_id: The employee's ID, e.g. "E1001".
    """
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        return f"No employee found with ID {employee_id}."
    return (
        f"{employee['name']} ({employee_id}) has "
        f"{employee['leave_balance_days']} leave days remaining."
    )


@mcp.tool()
def get_onboarding_checklist(employee_id: str) -> str:
    """Get the new-hire onboarding checklist and whether the employee is done.

    Args:
        employee_id: The employee's ID, e.g. "E1002".
    """
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        return f"No employee found with ID {employee_id}."

    status = "COMPLETE" if employee["onboarding_complete"] else "IN PROGRESS"
    steps = "\n".join(f"  - {step}" for step in ONBOARDING_CHECKLIST)
    return (
        f"Onboarding for {employee['name']} ({employee_id}): {status}\n"
        f"Checklist:\n{steps}"
    )


# ===========================================================================
# US COMPLIANCE TOOLS  (Darwinbox's weak spot — this is the standout part)
# ===========================================================================
def _resolve_state(employee_id: str, state: str):
    """Helper: figure out which state to use and load its rules."""
    employee = EMPLOYEES.get(employee_id) if employee_id else None
    code = (state or (employee["work_state"] if employee else "")).upper()
    rules = STATE_RULES.get(code)
    return employee, code, rules


@mcp.tool()
def check_state_tax_compliance(employee_id: str = "", state: str = "") -> str:
    """Check US state income-tax and payroll withholding rules.

    Useful when hiring in a new state or when an employee relocates.

    Args:
        employee_id: Optional employee ID, e.g. "E1001".
        state: Optional 2-letter state code, e.g. "CA". If blank, uses the
               employee's current work state.
    """
    employee, code, rules = _resolve_state(employee_id, state)
    if not rules:
        return f"No rules for state '{code}'. Supported: {', '.join(SUPPORTED_STATES)}."

    form = rules["withholding_form"] or "none (no state income tax)"
    move_note = ""
    if employee and state and code != employee["work_state"]:
        move_note = (
            f"\n⚠ Relocation detected: {employee['name']} is moving from "
            f"{employee['work_state']} to {code}. Update payroll withholding "
            f"and have them complete the new state's withholding form."
        )
    return (
        f"State: {code}\n"
        f"State income tax: {'YES' if rules['income_tax'] else 'NO'}\n"
        f"State withholding form: {form}\n"
        f"Notes: {rules['notes']}"
        f"{move_note}"
    )


@mcp.tool()
def check_minimum_wage(state: str) -> str:
    """Check the effective minimum wage for a US state (higher of state vs federal).

    Args:
        state: 2-letter state code, e.g. "TX".
    """
    code = state.upper()
    rules = STATE_RULES.get(code)
    if not rules:
        return f"No rules for state '{code}'. Supported: {', '.join(SUPPORTED_STATES)}."

    federal = FEDERAL_RULES["minimum_wage_usd"]
    state_wage = rules["min_wage_usd"]
    effective = max(state_wage, federal)
    governing = "federal" if federal >= state_wage else "state"
    return (
        f"State: {code}\n"
        f"State minimum wage: ${state_wage:.2f}/hr\n"
        f"Federal minimum wage: ${federal:.2f}/hr\n"
        f"Effective minimum wage: ${effective:.2f}/hr ({governing} rate applies)\n"
        f"Notes: {rules['notes']}"
    )


@mcp.tool()
def calculate_overtime_pay(hours_worked: float, hourly_rate: float) -> str:
    """Calculate a weekly paycheck including federal overtime (FLSA).

    Overtime is 1.5x pay for hours worked over 40 in a week.

    Args:
        hours_worked: Total hours worked in the week, e.g. 46.
        hourly_rate: Base hourly pay rate in USD, e.g. 20.0.
    """
    threshold = FEDERAL_RULES["overtime_threshold_hours"]
    multiplier = FEDERAL_RULES["overtime_multiplier"]

    regular_hours = min(hours_worked, threshold)
    overtime_hours = max(0.0, hours_worked - threshold)
    regular_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * hourly_rate * multiplier
    total = regular_pay + overtime_pay

    return (
        f"Hours worked: {hours_worked} (regular {regular_hours}, overtime {overtime_hours})\n"
        f"Base rate: ${hourly_rate:.2f}/hr\n"
        f"Regular pay: ${regular_pay:.2f}\n"
        f"Overtime pay (x{multiplier} over {threshold}h): ${overtime_pay:.2f}\n"
        f"TOTAL gross pay: ${total:.2f}"
    )


@mcp.tool()
def get_i9_everify_requirements(state: str = "") -> str:
    """Explain Form I-9 and E-Verify requirements for a US new hire.

    Args:
        state: Optional 2-letter state code, e.g. "AZ". If blank, gives federal-only info.
    """
    lines = [
        "Federal requirement: EVERY US new hire must complete Form I-9 "
        "(employment eligibility verification) within 3 business days of their start date.",
    ]
    if state:
        code = state.upper()
        rules = STATE_RULES.get(code)
        if not rules:
            return f"No rules for state '{code}'. Supported: {', '.join(SUPPORTED_STATES)}."
        if rules["everify_mandatory"]:
            lines.append(f"State ({code}): E-Verify is MANDATORY. {rules['notes']}")
        else:
            lines.append(f"State ({code}): E-Verify is not mandated statewide (federal contractors may still need it).")
    return "\n".join(lines)


# ===========================================================================
# INTEGRATION TOOL  (real Slack/email if configured, simulated otherwise)
# ===========================================================================
@mcp.tool()
def notify_manager(employee_id: str, message: str) -> str:
    """Send a notification to an employee's manager via Slack or email.

    Sends for real if SLACK_WEBHOOK_URL or SMTP_* env vars are configured;
    otherwise safely simulates the send.

    Args:
        employee_id: The employee's ID, e.g. "E1002".
        message: The message to send to the manager.
    """
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        return f"No employee found with ID {employee_id}."

    full_message = (
        f"[HR notification re: {employee['name']}] {message} "
        f"(manager: {employee['manager']})"
    )
    status = deliver(
        full_message,
        email_to=employee.get("manager_email"),
        subject=f"HR update for {employee['name']}",
    )
    return f"{status}\nRecipient: {employee['manager']} ({employee['manager_slack']})"


if __name__ == "__main__":
    mcp.run()
