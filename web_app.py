"""
Web dashboard for the HR Super Agent.

A tiny, dependency-free web UI (Python standard library only) that lets you click
through the same tools the MCP server exposes — great for a live demo or a
screen recording without needing to set up Claude Desktop.

Run it:   python web_app.py
Then open http://localhost:8000 in your browser.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import server as hr
from compliance_data import SUPPORTED_STATES

PORT = 8000

# Map a friendly action name -> a function that takes the posted args and
# returns a plain-text result. This is the whole "API".
DISPATCH = {
    "leave_balance":   lambda a: hr.get_leave_balance(a["employee_id"]),
    "onboarding":      lambda a: hr.get_onboarding_checklist(a["employee_id"]),
    "state_tax":       lambda a: hr.check_state_tax_compliance(a.get("employee_id", ""), a.get("state", "")),
    "min_wage":        lambda a: hr.check_minimum_wage(a["state"]),
    "overtime":        lambda a: hr.calculate_overtime_pay(float(a["hours"]), float(a["rate"])),
    "i9":              lambda a: hr.get_i9_everify_requirements(a.get("state", "")),
    "attrition":       lambda a: hr.predict_attrition_risk(a["employee_id"]),
    "pay_equity":      lambda a: hr.analyze_pay_equity(a.get("role", "")),
    "policy":          lambda a: hr.ask_hr_policy(a["question"]),
    "submit_request":  lambda a: hr.submit_approval_request(a["workflow_type"], a["requester"], float(a.get("amount", 0)), a.get("description", "")),
    "act_request":     lambda a: hr.act_on_approval(a["request_id"], a["decision"], a.get("approver", "")),
}

STATE_OPTIONS = "".join(f'<option value="{s}">{s}</option>' for s in SUPPORTED_STATES)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HR Super Agent — Dashboard</title>
<style>
  :root { --bg:#0f1220; --card:#1a1f36; --ink:#e8ecff; --muted:#9aa3c7;
          --accent:#6ea8fe; --good:#43d17a; --warn:#ffcc66; --bad:#ff6b6b; --line:#2a3050; }
  @media (prefers-color-scheme: light) {
    :root { --bg:#f4f6ff; --card:#ffffff; --ink:#141a33; --muted:#5a6488;
            --accent:#2b6cff; --line:#e2e7f5; }
  }
  * { box-sizing: border-box; }
  body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
         background: var(--bg); color: var(--ink); }
  header { padding: 22px 20px; border-bottom:1px solid var(--line); }
  header h1 { margin:0; font-size: 20px; }
  header p { margin:4px 0 0; color: var(--muted); font-size: 13px; }
  .wrap { max-width: 1100px; margin: 0 auto; padding: 18px 20px 60px;
          display:grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media (max-width: 800px){ .wrap { grid-template-columns: 1fr; } }
  .card { background: var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; }
  .card h2 { margin:0 0 10px; font-size: 14px; letter-spacing:.02em; text-transform: uppercase; color: var(--muted); }
  label { display:block; font-size:12px; color:var(--muted); margin:8px 0 3px; }
  input, select, button, textarea { font: inherit; }
  input, select, textarea { width:100%; padding:9px 10px; border-radius:9px;
          border:1px solid var(--line); background: transparent; color: var(--ink); }
  .row { display:flex; gap:8px; }
  .row > * { flex:1; }
  button { margin-top:10px; padding:9px 12px; border-radius:9px; border:none;
           background: var(--accent); color:#001; font-weight:600; cursor:pointer; }
  button:hover { filter: brightness(1.08); }
  pre { white-space: pre-wrap; word-break: break-word; background: rgba(127,127,127,.08);
        border-radius:9px; padding:12px; font-size:12.5px; line-height:1.5; margin:10px 0 0; min-height: 20px; }
  .full { grid-column: 1 / -1; }
  .hint { font-size:11px; color:var(--muted); margin-top:6px; }
</style>
</head>
<body>
<header>
  <h1>🧑‍💼 HR Super Agent — Dashboard</h1>
  <p>An MCP server for HR automation · US compliance across all 50 states + DC · workforce analytics · semantic search · approval workflows</p>
</header>
<div class="wrap">

  <div class="card">
    <h2>Employee lookup</h2>
    <label>Employee ID</label>
    <select id="emp">
      <option>E1001</option><option>E1002</option><option>E1003</option>
      <option>E1004</option><option>E1005</option>
    </select>
    <div class="row">
      <button onclick="run('leave_balance',{employee_id:val('emp')})">Leave balance</button>
      <button onclick="run('onboarding',{employee_id:val('emp')})">Onboarding</button>
    </div>
    <button onclick="run('attrition',{employee_id:val('emp')})">🧠 Predict attrition risk</button>
    <pre id="out_emp"></pre>
  </div>

  <div class="card">
    <h2>US compliance (all 50 states + DC)</h2>
    <label>State</label>
    <select id="state">__STATES__</select>
    <div class="row">
      <button onclick="run('min_wage',{state:val('state')})">Min wage</button>
      <button onclick="run('state_tax',{state:val('state')})">State tax</button>
      <button onclick="run('i9',{state:val('state')})">I-9 / E-Verify</button>
    </div>
    <pre id="out_comp"></pre>
  </div>

  <div class="card">
    <h2>Overtime calculator (FLSA)</h2>
    <div class="row">
      <div><label>Hours worked</label><input id="hrs" type="number" value="46"></div>
      <div><label>Hourly rate ($)</label><input id="rate" type="number" value="20"></div>
    </div>
    <button onclick="run('overtime',{hours:val('hrs'),rate:val('rate')})">Calculate gross pay</button>
    <pre id="out_ot"></pre>
  </div>

  <div class="card">
    <h2>Pay-equity analysis</h2>
    <label>Role (blank = all)</label>
    <input id="role" value="Senior Software Engineer">
    <button onclick="run('pay_equity',{role:val('role')})">⚖️ Analyze pay equity</button>
    <pre id="out_pay"></pre>
  </div>

  <div class="card full">
    <h2>Ask HR policy (semantic search)</h2>
    <input id="q" value="do unused vacation days carry over?" onkeydown="if(event.key==='Enter')run('policy',{question:val('q')},'out_pol')">
    <button onclick="run('policy',{question:val('q')},'out_pol')">🔍 Search policy</button>
    <div class="hint">Try: "can I work remotely?", "parental leave", "expense receipt rules"</div>
    <pre id="out_pol"></pre>
  </div>

  <div class="card full">
    <h2>Approval workflow</h2>
    <div class="row">
      <div><label>Type</label>
        <select id="wf"><option value="expense_report">expense_report</option><option value="leave_request">leave_request</option></select>
      </div>
      <div><label>Requester</label><input id="req" value="John Miller"></div>
      <div><label>Amount ($)</label><input id="amt" type="number" value="6000"></div>
    </div>
    <button onclick="run('submit_request',{workflow_type:val('wf'),requester:val('req'),amount:val('amt'),description:'demo'},'out_wf')">Submit request</button>
    <div class="hint">A $6,000 expense auto-routes Manager → Finance → HR/VP. Then approve a step:</div>
    <div class="row">
      <div><label>Request ID</label><input id="rid" value="REQ-0001"></div>
      <div><label>Decision</label><select id="dec"><option>approve</option><option>reject</option></select></div>
      <div><label>Approver</label><input id="apr" value="Sara Lopez"></div>
    </div>
    <button onclick="run('act_request',{request_id:val('rid'),decision:val('dec'),approver:val('apr')},'out_wf')">Act on request</button>
    <pre id="out_wf"></pre>
  </div>

</div>
<script>
  function val(id){ return document.getElementById(id).value; }
  function outFor(tool){
    return {leave_balance:'out_emp',onboarding:'out_emp',attrition:'out_emp',
            min_wage:'out_comp',state_tax:'out_comp',i9:'out_comp',
            overtime:'out_ot',pay_equity:'out_pay',policy:'out_pol',
            submit_request:'out_wf',act_request:'out_wf'}[tool] || 'out_emp';
  }
  async function run(tool, args, outId){
    const el = document.getElementById(outId || outFor(tool));
    el.textContent = '...';
    try {
      const res = await fetch('/api', {method:'POST', headers:{'Content-Type':'application/json'},
                                       body: JSON.stringify({tool, args})});
      const data = await res.json();
      el.textContent = data.result || data.error || '(no output)';
    } catch(e){ el.textContent = 'Error: ' + e; }
  }
</script>
</body>
</html>
""".replace("__STATES__", STATE_OPTIONS)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # keep the console quiet

    def do_GET(self):
        self._send(200, "text/html", PAGE.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            tool = payload.get("tool")
            args = payload.get("args", {})
            fn = DISPATCH.get(tool)
            if not fn:
                body = {"error": f"Unknown tool '{tool}'."}
            else:
                body = {"result": fn(args)}
        except Exception as exc:
            body = {"error": str(exc)}
        self._send(200, "application/json", json.dumps(body).encode("utf-8"))

    def _send(self, code, ctype, data):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"HR Super Agent dashboard running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
