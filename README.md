# HR Super Agent — an MCP server for HR automation

An **MCP (Model Context Protocol) server** that exposes HR capabilities as tools
any AI agent can call — including agents built on Darwinbox's own MCP platform.

Instead of a person clicking through an HR portal, an AI assistant can now:
answer leave questions, run onboarding, check US state payroll compliance, and
notify managers — all by calling this server's tools.

## Why this matters for Darwinbox

Darwinbox is the **first HCM platform in the world to ship an MCP server** and is
investing heavily in agentic AI ("Super Agent"). This project plugs directly into
that vision by adding tools an agent can use, and it targets Darwinbox's two known
gaps as it expands into the US market:

- **US payroll/compliance depth** — reviewers rate this as a weak spot vs. Rippling.
  The `check_state_tax_compliance` tool shows how state-specific rules (TX vs CA vs NY)
  can be handled automatically when an employee moves.
- **Fewer integrations** — the `notify_manager` tool shows a clean pattern for
  wiring HR events into external tools like Slack.

## The tools

| Tool | What it does | Idea it demonstrates |
|------|--------------|----------------------|
| `get_leave_balance` | Look up remaining leave days | HR data access |
| `get_onboarding_checklist` | Show onboarding steps + status | Onboarding automation |
| `check_state_tax_compliance` | US state tax/payroll rules, flags moves | **US compliance (gap-filler)** |
| `notify_manager` | Notify a manager (simulated Slack) | **Integration (gap-filler)** |

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Quick self-test (no AI needed):
python test_server.py

# Run as a real MCP server:
python server.py
```

## Connect it to Claude Desktop (see the AI actually use it)

Add this to your Claude Desktop MCP config, then restart Claude Desktop and ask it
HR questions like *"How many leave days does E1003 have?"*:

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

## What's real vs. simulated

- The **MCP server and tools are 100% real** — the same protocol Darwinbox uses.
- The **HR data is sample data** (a fake company) so it runs with zero setup.
- The **Slack notification is simulated** so no API keys are needed to demo it.

Swapping the sample data for a real database and the simulated Slack call for the
real Slack API are the natural next steps.

## Roadmap

- [ ] Replace sample data with a real database (Darwinbox uses MongoDB)
- [ ] Real Slack integration
- [ ] More US states + federal rules in the compliance tool
- [ ] Add authentication / per-employee permissions
