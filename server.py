"""
HR Super Agent — MCP Server
===========================

This is an MCP (Model Context Protocol) server that exposes HR "tools".
Any MCP-compatible AI agent (Claude Desktop, or Darwinbox's Super Agent)
can connect to this server and call these tools to get real work done.

Each function below decorated with @mcp.tool() becomes a tool the AI can use.
That is the whole trick: an MCP tool is just a normal Python function with a
label on it, plus a clear description so the AI knows when to use it.

Run it with:   python server.py
"""

from mcp.server.fastmcp import FastMCP

from sample_data import (
    EMPLOYEES,
    ONBOARDING_CHECKLIST,
    US_STATE_TAX_RULES,
)

# Create the server. The name shows up in the AI client's tool list.
mcp = FastMCP("HR Super Agent")


# ---------------------------------------------------------------------------
# TOOL 1 (Option 1: HR data) — look up an employee's leave balance
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TOOL 2 (Option 1: HR data) — onboarding checklist + progress
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TOOL 3 (Option 2: US compliance) — check state payroll/tax rules
# This targets Darwinbox's known weak spot: deep US payroll compliance.
# ---------------------------------------------------------------------------
@mcp.tool()
def check_state_tax_compliance(employee_id: str, new_state: str = "") -> str:
    """Check US state income-tax and payroll rules for an employee.

    Useful when an employee moves states, since payroll must be updated.

    Args:
        employee_id: The employee's ID, e.g. "E1001".
        new_state: Optional 2-letter state code the employee is moving to,
                   e.g. "CA". If left blank, uses their current work state.
    """
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        return f"No employee found with ID {employee_id}."

    state = (new_state or employee["work_state"]).upper()
    rules = US_STATE_TAX_RULES.get(state)
    if not rules:
        return (
            f"No compliance rules loaded for state '{state}'. "
            f"Supported: {', '.join(US_STATE_TAX_RULES)}."
        )

    forms = ", ".join(rules["extra_forms"]) if rules["extra_forms"] else "none"
    moving_note = ""
    if new_state and state != employee["work_state"]:
        moving_note = (
            f"\n⚠ Payroll change needed: {employee['name']} is moving from "
            f"{employee['work_state']} to {state}. Update withholding."
        )
    return (
        f"State: {state}\n"
        f"State income tax: {'YES' if rules['state_income_tax'] else 'NO'}\n"
        f"Note: {rules['note']}\n"
        f"Extra forms required: {forms}"
        f"{moving_note}"
    )


# ---------------------------------------------------------------------------
# TOOL 4 (Option 3: integration) — notify an employee's manager
# In a real system this would call Slack's API. Here we simulate it so the
# demo runs with zero setup and no API keys.
# ---------------------------------------------------------------------------
@mcp.tool()
def notify_manager(employee_id: str, message: str) -> str:
    """Send a notification to an employee's manager (simulated Slack message).

    Args:
        employee_id: The employee's ID, e.g. "E1002".
        message: The message to send to the manager.
    """
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        return f"No employee found with ID {employee_id}."

    # Real integration would POST to Slack here. We simulate the send.
    return (
        f"✅ Sent to {employee['manager']} ({employee['manager_slack']}): "
        f'"{message}"'
    )


# ---------------------------------------------------------------------------
# Start the server when this file is run directly.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
