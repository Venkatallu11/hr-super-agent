"""
Multi-level approval workflow engine.

Approval chains are one of the fiddliest parts of any HR system: a leave request
might need just a manager, but an expense over $5,000 might need manager →
finance → HR. Real platforms build heavy "workflow builders" for this.

Here is a small, readable state machine that captures the essential idea:
a request moves step-by-step through an ordered chain of approvers, and each
approval advances it until it's fully APPROVED (or someone rejects it).

State is kept in memory for the demo; a real system would persist it.
"""

import itertools

# --- Workflow templates: which approvers, in which order --------------------
# A step can be conditional on an amount (e.g. only needed above a threshold).
WORKFLOW_TEMPLATES = {
    "leave_request": [
        {"approver": "Manager", "required_if_amount_gte": 0},
    ],
    "expense_report": [
        {"approver": "Manager", "required_if_amount_gte": 0},
        {"approver": "Finance", "required_if_amount_gte": 500},
        {"approver": "HR/VP",  "required_if_amount_gte": 5000},
    ],
}

# In-memory store of live requests.
_REQUESTS: dict[str, dict] = {}
_ID_COUNTER = itertools.count(1)


def _build_chain(workflow_type: str, amount: float) -> list[str]:
    """Pick which approvers actually apply, based on the amount."""
    template = WORKFLOW_TEMPLATES[workflow_type]
    return [
        step["approver"]
        for step in template
        if amount >= step["required_if_amount_gte"]
    ]


def submit_request(workflow_type: str, requester: str, amount: float = 0.0,
                   description: str = "") -> dict:
    """Create a new approval request and return its starting state."""
    if workflow_type not in WORKFLOW_TEMPLATES:
        return {"error": f"Unknown workflow '{workflow_type}'. "
                         f"Options: {', '.join(WORKFLOW_TEMPLATES)}."}

    chain = _build_chain(workflow_type, amount)
    request_id = f"REQ-{next(_ID_COUNTER):04d}"
    _REQUESTS[request_id] = {
        "id": request_id,
        "type": workflow_type,
        "requester": requester,
        "amount": amount,
        "description": description,
        "chain": chain,
        "current_step": 0,
        "status": "PENDING",
        "history": [],
    }
    return _status_view(request_id)


def act_on_request(request_id: str, decision: str, approver: str = "") -> dict:
    """Approve or reject the current step of a request.

    Args:
        request_id: e.g. "REQ-0001".
        decision: "approve" or "reject".
        approver: name of the person acting (optional, for the audit trail).
    """
    req = _REQUESTS.get(request_id)
    if not req:
        return {"error": f"No request found with ID {request_id}."}
    if req["status"] != "PENDING":
        return {"error": f"Request {request_id} is already {req['status']}."}

    step_name = req["chain"][req["current_step"]]
    decision = decision.lower()

    if decision == "reject":
        req["status"] = "REJECTED"
        req["history"].append(f"{step_name} ({approver or 'n/a'}) REJECTED")
        return _status_view(request_id)

    if decision == "approve":
        req["history"].append(f"{step_name} ({approver or 'n/a'}) approved")
        req["current_step"] += 1
        if req["current_step"] >= len(req["chain"]):
            req["status"] = "APPROVED"
        return _status_view(request_id)

    return {"error": "Decision must be 'approve' or 'reject'."}


def get_request_status(request_id: str) -> dict:
    req = _REQUESTS.get(request_id)
    if not req:
        return {"error": f"No request found with ID {request_id}."}
    return _status_view(request_id)


def _status_view(request_id: str) -> dict:
    req = _REQUESTS[request_id]
    if req["status"] == "PENDING":
        waiting_on = req["chain"][req["current_step"]]
        progress = f"step {req['current_step'] + 1} of {len(req['chain'])}"
    else:
        waiting_on = None
        progress = "complete"
    return {
        "id": req["id"],
        "type": req["type"],
        "requester": req["requester"],
        "amount": req["amount"],
        "approval_chain": req["chain"],
        "status": req["status"],
        "progress": progress,
        "waiting_on": waiting_on,
        "history": req["history"],
    }
