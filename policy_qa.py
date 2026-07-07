"""
HR policy Q&A with lightweight semantic search.

Big HR platforms advertise "semantic search" over policy documents as an
AI feature. Under the hood it's usually vector embeddings. Here we implement a
real, dependency-free version using TF-IDF + cosine similarity — the same core
idea (rank passages by relevance to a question), just simple enough to read in
one sitting and run anywhere.

Given a natural-language question, it returns the most relevant policy passage.
"""

import math
import re
from collections import Counter


# --- The "knowledge base": company HR policy passages -----------------------
# In production this would be thousands of chunks pulled from real documents.
POLICY_PASSAGES = [
    ("Paid Time Off",
     "Full-time employees accrue 1.5 paid leave days per month, up to a maximum "
     "of 18 days per year. Unused leave over 5 days does not carry into the next "
     "year. Leave requests should be submitted at least two weeks in advance."),
    ("Remote Work",
     "Employees may work remotely up to three days per week with manager approval. "
     "Fully remote arrangements require director sign-off and a home-office stipend "
     "of $500 is provided for eligible remote employees."),
    ("Parental Leave",
     "New parents are eligible for 12 weeks of paid parental leave following the "
     "birth or adoption of a child. Leave must be taken within the first 12 months "
     "and can be split into two blocks."),
    ("Expense Reimbursement",
     "Business expenses under $75 do not require a receipt. Expenses of $75 or more "
     "must include an itemized receipt and manager approval. Reimbursements are paid "
     "within two payroll cycles of approval."),
    ("Health Benefits",
     "Medical, dental, and vision coverage begins on the first day of the month "
     "after your start date. Open enrollment runs each November. Employees may add "
     "dependents within 30 days of a qualifying life event."),
    ("Overtime and Hours",
     "Non-exempt employees are paid 1.5 times their base rate for hours worked over "
     "40 in a week, in line with federal FLSA rules. Overtime must be approved by a "
     "manager in advance."),
]


# --- Tiny TF-IDF semantic search --------------------------------------------
_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


# Pre-compute document term frequencies and inverse document frequency once.
_DOCS = [(title, body, Counter(_tokenize(title + " " + body)))
         for title, body in POLICY_PASSAGES]
_N = len(_DOCS)
_IDF: dict[str, float] = {}
for _, _, _tf in _DOCS:
    for term in _tf:
        _IDF[term] = _IDF.get(term, 0) + 1
for term, df in _IDF.items():
    _IDF[term] = math.log((_N + 1) / (df + 1)) + 1  # smoothed idf


def _vector(counts: Counter) -> dict[str, float]:
    """Turn term counts into a TF-IDF weighted vector."""
    return {term: freq * _IDF.get(term, math.log(_N + 1) + 1)
            for term, freq in counts.items()}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def search_policy(question: str) -> dict:
    """Return the most relevant HR policy passage for a natural-language question."""
    query_vec = _vector(Counter(_tokenize(question)))

    scored = []
    for title, body, tf in _DOCS:
        score = _cosine(query_vec, _vector(tf))
        scored.append((score, title, body))
    scored.sort(reverse=True, key=lambda x: x[0])

    best_score, best_title, best_body = scored[0]
    if best_score < 0.03:
        return {
            "question": question,
            "answer": "I couldn't find a relevant policy. Please contact HR directly.",
            "confidence": round(best_score, 3),
        }

    return {
        "question": question,
        "matched_policy": best_title,
        "answer": best_body,
        "confidence": round(best_score, 3),
        "runner_up": scored[1][1] if len(scored) > 1 else None,
    }
