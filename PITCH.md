# Your pitch — HR Super Agent → Darwinbox

Copy/adapt these when reaching out. Keep it honest: this is a **demo built on
public research** with sample data — say so if asked. That honesty is a plus.

---

## 1. Short LinkedIn message (to a Darwinbox recruiter / US hiring manager)

> Hi [Name] — I saw Darwinbox is scaling fast in the US and just shipped the
> first MCP server in HCM. That got me excited, so I built a small MCP server of
> my own that plugs HR tools into any AI agent: US payroll compliance across all
> 50 states, an explainable attrition-risk model, semantic policy search, and
> multi-level approval workflows. It's a demo, but it targets the exact US gaps
> I read about (payroll depth, integrations). Would love to show you a 60-second
> video — is there a good person on the US team to share it with?
>
> Repo: https://github.com/Venkatallu11/hr-super-agent

*(Under ~90 words on purpose — short messages get replies.)*

---

## 2. Application / cover-letter paragraph

> I'm applying because Darwinbox's US expansion and its bet on agentic AI line up
> exactly with what I like to build. To learn your problem space, I built an MCP
> server — the same protocol your Super Agent uses — that exposes HR capabilities
> as tools any AI can call. It covers US payroll compliance for all 50 states + DC
> (income tax, minimum wage, FLSA overtime, I-9/E-Verify), an *explainable*
> attrition-risk model, TF-IDF semantic search over HR policies, and a
> multi-level approval-workflow engine. It's a demo with sample data, but it was
> a deliberate way to show I understand both the technology and the US-market
> gaps you're closing. Code and a live dashboard are on my GitHub.

---

## 3. Interview talking points

**Why I built it**
- Darwinbox is the first HCM to ship an MCP server and is investing in "Super
  Agent" agentic AI. I wanted to build *in that ecosystem*, not just talk about it.

**What it shows technically**
- MCP server design (13 tools with clear schemas an AI can reason about).
- Explainable ML-style scoring (attrition) — no black box, every point justified.
- Information retrieval (TF-IDF + cosine) built from scratch, no libraries.
- A small state machine (approval workflows) and a real integration pattern
  (Slack/email with safe fallback).
- Zero-dependency web dashboard (Python stdlib) for a live demo.

**How it maps to your gaps**
- Reviewers rate US payroll/compliance and integrations as Darwinbox's weak
  spots vs. Rippling. Those are the two areas I leaned into hardest.

**What I'd do next / honesty**
- The data is illustrative sample data; production would pull from a maintained
  legal DB and a real employee store (you use MongoDB). I designed the code so
  swapping those in is straightforward — the roadmap in the README lists it.

---

## 4. Where to send it

- Darwinbox careers (US): https://darwinbox.com/en-us/careers
- LinkedIn: search "Darwinbox" + "United States" for recruiters / eng managers
- Attach: the repo link + a 30–60s screen recording (see `DEMO.md`)
