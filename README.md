# HR Super Agent — an MCP server for HR automation

An **MCP (Model Context Protocol) server** that exposes HR capabilities as tools
any AI agent can call — including agents built on Darwinbox's own MCP platform.

Instead of a person clicking through an HR portal, an AI assistant can now:
answer leave questions, run onboarding, handle **US payroll compliance**, and
notify managers — all by calling this server's tools.

```
                  ┌─────────────────────────┐
   Employee  ───► │   AI HR Agent (brain)   │
   asks a         └───────────┬─────────────┘
   question                   │ picks the right tool
        ┌──────────────┬──────┴───────┬────────────────┐
        ▼              ▼              ▼                 ▼
   ┌─────────┐  ┌────────────┐  ┌──────────┐   ┌──────────────┐
   │ HR data │  │ US payroll │  │ Overtime │   │ Integrations │
   │ leave / │  │ compliance │  │ / wage   │   │ Slack /email │
   │ onboard │  │ (states)   │  │ math     │   │ (real)       │
   └─────────┘  └────────────┘  └──────────┘   └──────────────┘
```

## Why this matters for Darwinbox

Darwinbox is the **first HCM platform in the world to ship an MCP server** and is
investing heavily in agentic AI ("Super Agent"). This project plugs directly into
that vision and targets Darwinbox's two known gaps as it expands into the US:

- **US payroll/compliance depth** — rated a weak spot vs. Rippling. This server
  handles state income tax, minimum wage (state vs federal), FLSA overtime, and
  I-9/E-Verify rules across **all 50 states + DC**.
- **Fewer integrations** — the `notify_manager` tool is a real, configurable
  Slack/email connector, not a fake stub.

## The tools

| Tool | What it does |
|------|--------------|
| `get_leave_balance` | Look up remaining leave days |
| `get_onboarding_checklist` | Show onboarding steps + status |
| `check_state_tax_compliance` | State income tax + withholding form; flags relocations |
| `check_minimum_wage` | Effective minimum wage (higher of state vs federal) |
| `calculate_overtime_pay` | Weekly gross pay with FLSA overtime (1.5x over 40h) |
| `get_i9_everify_requirements` | Federal I-9 + state E-Verify rules |
| `notify_manager` | Notify a manager via **real** Slack/email (or simulated) |

### Advanced capabilities — hard problems, made simple

These are the features enterprise HR suites sell as premium, black-box modules.
Here they're transparent, dependency-free, and easy to read:

| Tool | What it does | The "hard problem" it tackles |
|------|--------------|-------------------------------|
| `predict_attrition_risk` | 0-100 flight-risk score with a full explanation of every factor | **Explainable** workforce analytics (no black box) |
| `analyze_pay_equity` | Flags below-median pay and gender pay gaps within a role | Pay-equity compliance (a hot US legal topic) |
| `ask_hr_policy` | Answers natural-language policy questions | **Semantic search** (real TF-IDF + cosine, pure Python) |
| `submit_approval_request` / `act_on_approval` / `get_approval_status` | Routes requests through multi-level approval chains | Workflow automation (a $6k expense auto-routes Manager→Finance→HR/VP) |

## See it in action (no setup, no API key)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python demo.py         # watch an AI agent use the tools on real scenarios
python test_server.py  # verify all 13 tools register and run
```

`demo.py` prints a full agent conversation where every tool result is real.
It's the quickest way to *show* the project working (great for a screenshot).

### Or launch the web dashboard

```bash
python web_app.py    # then open http://localhost:8000
```

A clickable dashboard (Python standard library only — no extra dependencies)
that exercises every tool: employee lookup, all-50-state compliance, the
overtime calculator, attrition risk, pay equity, policy search, and approval
workflows. Perfect for a live demo or a screen recording. See `DEMO.md` for a
suggested recording script.

## Connect it to Claude Desktop (chat with your HR agent)

Add this to your Claude Desktop MCP config, restart Claude Desktop, then ask
things like *"I'm moving from CA to TX, does my paycheck change?"*:

```json
{
  "mcpServers": {
    "hr-super-agent": {
      "command": "/full/path/to/.venv/bin/python",
      "args": ["/full/path/to/server.py"]
    }
  }
}
```

## Turn on real notifications (optional)

The `notify_manager` tool sends for real when you configure either channel via
environment variables — otherwise it safely simulates the send:

```bash
# Slack:
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"

# or email (e.g. Gmail app password):
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="you@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

## What's real vs. sample

- The **MCP server, all 13 tools, the analytics/semantic-search/workflow logic,
  the overtime/wage math, and the Slack/email
  integration are 100% real** — the same protocol Darwinbox uses.
- The **employee records are sample data** so it runs anywhere with zero setup.
- The **compliance rules are simplified/illustrative** (see `compliance_data.py`);
  a production version would pull from a maintained legal database.

## Project layout

| File | Purpose |
|------|---------|
| `server.py` | The MCP server and its 13 tools |
| `compliance_data.py` | US federal + all-50-states + DC payroll/compliance rules |
| `web_app.py` | Interactive web dashboard (stdlib only, no dependencies) |
| `analytics.py` | Explainable attrition risk + pay-equity analysis |
| `policy_qa.py` | Semantic policy search (TF-IDF + cosine, no ML libs) |
| `workflows.py` | Multi-level approval workflow engine |
| `integrations.py` | Real Slack/email connector with safe fallback |
| `sample_data.py` | Sample employees + onboarding checklist |
| `demo.py` | Scripted agent walkthrough (real tool calls) |
| `test_server.py` | Smoke test for all tools |

## Roadmap

- [x] Expand to all 50 states + DC
- [ ] Add local (city/county) payroll rules
- [ ] Replace sample data with a real database (Darwinbox uses MongoDB)
- [ ] Add authentication / per-employee permissions
- [ ] Add a short demo video
