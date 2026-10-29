"""Deterministic scoring engine. No AI here: same inputs -> same output.
Reads criteria.json (admin-defined) and extractions.json (validated AI output, values only).
Run: python score.py
"""
import json

crit = json.load(open("criteria.json"))
ext = json.load(open("extractions.json"))
W, S = crit["weights"], crit["scales"]

# 1. Mandatory gate (pass/fail)
status, why = {}, {}
for k, e in ext.items():
    if not e["licence_held_by_bidder"]:
        status[k], why[k] = "ineligible", "licence not held by bidder"
    elif not e["wsib_and_insurance"]:
        status[k], why[k] = "ineligible", "WSIB/insurance not confirmed"
    else:
        status[k] = "eligible"

# 2. Flags (never silently fixed)
for k, e in ext.items():
    notes = []
    if e["weeks"] is None: notes.append("no timeline stated")
    elif e["weeks"] > crit["max_weeks"]: notes.append("over 16 weeks")
    if e["price"] > crit["budget_ceiling_cad"]: notes.append("over budget")
    if e.get("window_unclear"): notes.append("install window unclear (some may be older than 5 years)")
    if e["injection"]: notes.append("embedded instruction aimed at reviewers")
    why[k] = (why.get(k, "") + "; ".join(notes)).strip("; ")

# 3. Relative benchmarks use eligible bids only (so an ineligible cheap bid cannot skew scores)
elig = [k for k in ext if status[k] == "eligible"]
best_price = min(ext[k]["price"] for k in elig)
best_weeks = min(ext[k]["weeks"] for k in elig if ext[k]["weeks"])

def sub_scores(e):
    team = sum([e["lead"], e["crew"], e["safety"], e["monitoring"]]) * 25
    return {
        "experience": min(e["installs"] / S["experience_full_marks_at"], 1) * 100,
        "price": best_price / e["price"] * 100,
        "timeline": 0 if e["weeks"] is None else best_weeks / e["weeks"] * 100,  # missing = 0, never guessed
        "warranty": min(e["panel_yrs"] / S["panel_warranty_full_years"], 1) * 50
                    + min(e["work_yrs"] / S["workmanship_full_years"], 1) * 50,
        "team": team,
    }

results = {}
for k in elig:
    ss = sub_scores(ext[k])
    total = sum(ss[c] * W[c] / 100 for c in W)
    results[k] = {"total": round(total, 1), "sub": {c: round(v, 1) for c, v in ss.items()}}

# 4. Rank: flagged-for-missing-data bids are held out of the ranked list
ranked = sorted([k for k in elig if ext[k]["weeks"] is not None],
                key=lambda k: (-results[k]["total"], -results[k]["sub"]["experience"], ext[k]["price"]))
for i, k in enumerate(ranked, 1):
    print(f"#{i} {k}  {results[k]['total']:>5}  {results[k]['sub']}  {why[k]}")
for k in ext:
    if k not in ranked:
        print(f"--  {k}  {status[k]}  {results.get(k, {}).get('total', '')}  {why[k]}")
