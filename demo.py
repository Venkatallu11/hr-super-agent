"""
Demo: an AI HR agent handling real employee requests using this server's tools.

This simulates what happens when an AI assistant (Claude, or Darwinbox's Super
Agent) is connected to our MCP server. For each employee question, the agent
picks the right tool, calls it, and gives a natural answer.

The tool CALLS AND RESULTS BELOW ARE 100% REAL — they run the actual server
functions. Only the AI's wording around them is scripted, so the demo is
reproducible without needing an API key.

Run it with:   python demo.py
"""

import server as hr  # the real MCP tools live here


def turn(user_msg: str, tool_name: str, tool_result: str, agent_reply: str):
    print(f"\n👤 Employee: {user_msg}")
    print(f"   🔧 agent calls tool → {tool_name}")
    print("   ┌─ tool result ─────────────────────────────")
    for line in tool_result.splitlines():
        print(f"   │ {line}")
    print("   └───────────────────────────────────────────")
    print(f"🤖 HR Agent: {agent_reply}")


def main():
    print("=" * 60)
    print("  HR SUPER AGENT — live tool demo")
    print("  (AI assistant connected to the MCP server)")
    print("=" * 60)

    # 1) Simple HR data question
    turn(
        "How many vacation days do I have left? I'm E1002.",
        "get_leave_balance(E1002)",
        hr.get_leave_balance("E1002"),
        "You have 4 leave days remaining. Want me to help you plan time off?",
    )

    # 2) US compliance — relocation (Darwinbox's weak spot)
    turn(
        "I'm relocating from California to Texas — does my paycheck change?",
        "check_state_tax_compliance(E1002, state=TX)",
        hr.check_state_tax_compliance("E1002", "TX"),
        "Good news: Texas has no state income tax, so your state withholding "
        "stops. I've flagged payroll to update your records for the move.",
    )

    # 3) US compliance — overtime math
    turn(
        "I worked 46 hours last week at $20/hr. What's my gross pay?",
        "calculate_overtime_pay(46, 20)",
        hr.calculate_overtime_pay(46, 20),
        "Your gross pay is $980: 40 regular hours at $20, plus 6 overtime "
        "hours at time-and-a-half ($30/hr).",
    )

    # 4) US compliance — minimum wage
    turn(
        "We're hiring a warehouse worker in Washington state. What's the minimum wage?",
        "check_minimum_wage(WA)",
        hr.check_minimum_wage("WA"),
        "In Washington the effective minimum wage is $16.28/hr — well above "
        "the federal $7.25 floor, so the state rate governs.",
    )

    # 5) US compliance — I-9 / E-Verify
    turn(
        "We just hired someone in Arizona. Any employment-eligibility steps?",
        "get_i9_everify_requirements(AZ)",
        hr.get_i9_everify_requirements("AZ"),
        "Yes — complete Form I-9 within 3 business days, and note that "
        "E-Verify is mandatory in Arizona.",
    )

    # 6) Integration — notify a manager (real send if configured, else simulated)
    turn(
        "Please ask my manager to approve my leave request.",
        "notify_manager(E1002, ...)",
        hr.notify_manager("E1002", "John requests approval for 3 days of leave."),
        "Done — I've notified your manager. You'll hear back once it's approved.",
    )

    print("\n" + "-" * 60)
    print("  ADVANCED: analytics, semantic search, workflows")
    print("-" * 60)

    # 7) Analytics — explainable attrition risk (HR manager asking)
    turn(
        "Which of my reports is most at risk of quitting, and why?",
        "predict_attrition_risk(E1005)",
        hr.predict_attrition_risk("E1005"),
        "Diego is HIGH risk (77/100), mainly low engagement and burnout signals. "
        "I'd suggest a check-in and a comp review.",
    )

    # 8) Analytics — pay equity (compliance-sensitive)
    turn(
        "Run a pay-equity check on our Senior Software Engineers.",
        "analyze_pay_equity('Senior Software Engineer')",
        hr.analyze_pay_equity("Senior Software Engineer"),
        "Heads up: there's a 12% median gender pay gap in that role worth reviewing.",
    )

    # 9) Semantic policy search
    turn(
        "Do my unused vacation days carry over to next year?",
        "ask_hr_policy('do unused vacation days carry over?')",
        hr.ask_hr_policy("do unused vacation days carry over to next year?"),
        "Only up to 5 days carry over — anything above that is lost at year-end.",
    )

    # 10) Multi-level approval workflow
    turn(
        "I need to submit a $6,000 conference travel expense.",
        "submit_approval_request('expense_report', 'John Miller', 6000, ...)",
        hr.submit_approval_request("expense_report", "John Miller", 6000, "Conference travel"),
        "Submitted. Because it's over $5,000 it routes through Manager → Finance → "
        "HR/VP. It's now waiting on your manager.",
    )

    print("\n" + "=" * 60)
    print("  End of demo — every tool result above was real.")
    print("=" * 60)


if __name__ == "__main__":
    main()
