# HR Super Agent — an MCP server for HR automation

An **MCP (Model Context Protocol) server** that exposes HR capabilities as tools
any AI agent can call — including agents built on Darwinbox's own MCP platform.

Instead of a person clicking through an HR portal, an AI assistant can answer
leave questions, run onboarding, handle **US payroll compliance across all 50
states + DC**, predict attrition, check pay equity, search HR policy, route
approval workflows, and notify managers — all by calling this server's tools.

**▶ Live interactive demo:** https://claude.ai/code/artifact/b18155a7-6e1f-4208-a990-459c86d62fb9

```
                     ┌──────────────────────────┐
   Employee / HR ──► │    AI HR Agent (brain)    │  ◄─ Claude Desktop,
   asks in plain     └────────────┬─────────────┘     Darwinbox Super Agent,
   English                        │ picks the right    any MCP client
                                  │ tool
     ┌───────────┬────────────┬───┴────────┬─────────────┬──────────────┐
     ▼           ▼            ▼            ▼             ▼              ▼
 ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
 │ HR data│ │ US payroll│ │ Workforce│ │ Semantic │ │ Approval │ │Integrations│
 │ leave /│ │ compliance│ │ analytics│ │ policy   │ │ workflow │ │ Slack/email│
 │onboard │ │ 50 + DC   │ │ risk/pay │ │ search   │ │ engine   │ │ (real)     │
 └────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └────────────┘
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

## Features at a glance

- ✅ **13 AI-callable tools** across 6 capability areas
- ✅ **All 50 states + DC** payroll/compliance coverage
- ✅ **Explainable** attrition-risk model (no black box)
- ✅ **Pay-equity** analysis incl. gender pay gap
- ✅ **Semantic search** over HR policies (TF-IDF + cosine, no ML libraries)
- ✅ **Multi-level approval workflow** engine (amount-based routing)
- ✅ **Real** Slack/email integration with a safe simulated fallback
- ✅ **Zero-dependency web dashboard** (Python standard library only)
- ✅ A scripted **agent demo** where every tool result is real

## The 13 tools

### Core HR
| Tool | What it does |
|------|--------------|
| `get_leave_balance` | Look up remaining leave days |
| `get_onboarding_checklist` | Show onboarding steps + status |

### US compliance (all 50 states + DC)
| Tool | What it does |
|------|--------------|
| `check_state_tax_compliance` | State income tax + withholding form; flags relocations |
| `check_minimum_wage` | Effective minimum wage (higher of state vs federal) |
| `calculate_overtime_pay` | Weekly gross pay with FLSA overtime (1.5x over 40h) |
| `get_i9_everify_requirements` | Federal I-9 + state E-Verify rules |

### Advanced — hard problems, made simple
These are the features enterprise HR suites sell as premium, black-box modules.
Here they're transparent, dependency-free, and easy to read:

| Tool | What it does | The "hard problem" it tackles |
|------|--------------|-------------------------------|
| `predict_attrition_risk` | 0-100 flight-risk score with a full explanation of every factor | **Explainable** workforce analytics (no black box) |
| `analyze_pay_equity` | Flags below-median pay and gender pay gaps within a role | Pay-equity compliance (a hot US legal topic) |
| `ask_hr_policy` | Answers natural-language policy questions | **Semantic search** (real TF-IDF + cosine, pure Python) |
| `submit_approval_request` / `act_on_approval` / `get_approval_status` | Routes requests through multi-level approval chains | Workflow automation (a $6k expense auto-routes Manager→Finance→HR/VP) |

### Integration
| Tool | What it does |
|------|--------------|
| `notify_manager` | Notify a manager via **real** Slack/email (or simulated) |

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python demo.py         # watch an AI agent use the tools on real scenarios
python test_server.py  # verify all 13 tools register and run
python web_app.py      # launch the web dashboard at http://localhost:8000
```

- **`demo.py`** prints a full agent conversation where every tool result is real —
  the quickest way to *show* the project working (great for a screenshot).
- **`web_app.py`** is a clickable dashboard (Python standard library only, no extra
  dependencies) that exercises every tool. Great for a live demo or screen recording.
- **`showcase.html`** is a single self-contained page (real outputs embedded) you can
  open directly or host on GitHub Pages — it's the same page as the live demo link above.

See **`DEMO.md`** for step-by-step recording scripts.

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

- The **MCP server, all 13 tools, the analytics / semantic-search / workflow logic,
  the overtime/wage math, and the Slack/email integration are 100% real** — the same
  protocol Darwinbox uses.
- The **employee records are sample data** so it runs anywhere with zero setup.
- The **compliance rules are simplified/illustrative** (see `compliance_data.py`);
  a production version would pull from a maintained legal database.

## Project layout

| File | Purpose |
|------|---------|
| `server.py` | The MCP server and its 13 tools |
| `compliance_data.py` | US federal + all-50-states + DC payroll/compliance rules |
| `analytics.py` | Explainable attrition risk + pay-equity analysis |
| `policy_qa.py` | Semantic policy search (TF-IDF + cosine, no ML libs) |
| `workflows.py` | Multi-level approval workflow engine |
| `integrations.py` | Real Slack/email connector with safe fallback |
| `sample_data.py` | Sample employees + onboarding checklist |
| `web_app.py` | Interactive web dashboard (stdlib only, no dependencies) |
| `showcase.html` | Self-contained shareable demo page (real outputs embedded) |
| `demo.py` | Scripted agent walkthrough (real tool calls) |
| `test_server.py` | Smoke test for all tools |
| `DEMO.md` | Recording guide (terminal, web, Claude Desktop) |
| `PITCH.md` | LinkedIn message, application blurb, interview talking points |

## Documentation

- **`DEMO.md`** — three ways to demo the project and a suggested recording script.
- **`PITCH.md`** — ready-to-send outreach and interview material for Darwinbox.

## Roadmap

- [x] Core HR tools (leave, onboarding)
- [x] US compliance across all 50 states + DC
- [x] Real Slack/email integration
- [x] Explainable attrition risk + pay-equity analysis
- [x] Semantic policy search
- [x] Multi-level approval workflows
- [x] Web dashboard + shareable showcase
- [ ] Add local (city/county) payroll rules
- [ ] Replace sample data with a real database (Darwinbox uses MongoDB)
- [ ] Add authentication / per-employee permissions
- [ ] Record a short Claude Desktop demo video

---

*Built as a portfolio project studying Darwinbox's US expansion. It's a demo with
illustrative data, designed so a real employee store and legal data source drop
straight in.*
