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
  I-9/E-Verify rules across 15 states.
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

## See it in action (no setup, no API key)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python demo.py         # watch an AI agent use the tools on real scenarios
python test_server.py  # verify all 7 tools register and run
```

`demo.py` prints a full agent conversation where every tool result is real.
It's the quickest way to *show* the project working (great for a screenshot).

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

- The **MCP server, all 7 tools, the overtime/wage math, and the Slack/email
  integration are 100% real** — the same protocol Darwinbox uses.
- The **employee records are sample data** so it runs anywhere with zero setup.
- The **compliance rules are simplified/illustrative** (see `compliance_data.py`);
  a production version would pull from a maintained legal database.

## Project layout

| File | Purpose |
|------|---------|
| `server.py` | The MCP server and its 7 tools |
| `compliance_data.py` | US federal + 15-state payroll/compliance rules |
| `integrations.py` | Real Slack/email connector with safe fallback |
| `sample_data.py` | Sample employees + onboarding checklist |
| `demo.py` | Scripted agent walkthrough (real tool calls) |
| `test_server.py` | Smoke test for all tools |

## Roadmap

- [ ] Expand from 15 states to all 50 + local (city/county) rules
- [ ] Replace sample data with a real database (Darwinbox uses MongoDB)
- [ ] Add authentication / per-employee permissions
- [ ] Add a short demo video
