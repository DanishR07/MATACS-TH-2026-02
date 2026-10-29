"""Optional: run the extraction prompt (PROMPTS.md) on local sample files, validate, and write extractions.json.
Setup:  pip install anthropic python-dotenv   |  copy .env.example to .env and add your key
Usage:  put one text file per proposal in ./samples/ named A.txt ... E.txt (kept local, git-ignored), then: python extract.py
"""
import json, os, re, pathlib
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("MODEL", "claude-sonnet-5-5")
client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

md = pathlib.Path("../PROMPTS.md").read_text()
blocks = re.findall(r"```\n(.*?)```", md, re.S)
SYSTEM, USER_TMPL, SCHEMA = blocks[0], blocks[1], blocks[2]  # system message, user template, rendered schema

crit = json.load(open("criteria.json"))

def extract(text):
    user = (USER_TMPL.replace("{{category_name}}", crit["category"])
            .replace("{{project_summary}}", "150 kW rooftop solar, budget ceiling $260,000 CAD, 16 weeks max")
            .replace("{{today}}", "2026-10-29")
            .replace("{{criteria_fields_list}}", "See schema.")
            .replace("{{json_schema}}", SCHEMA)
            .replace("{{proposal_text_with_bidder_name_masked}}", text))
    msg = client.messages.create(model=MODEL, max_tokens=1500, temperature=0, system=SYSTEM,
                                 messages=[{"role": "user", "content": user}])
    return json.loads(msg.content[0].text)

def evidence_ok(node, source):
    """Code check: every evidence quote must appear verbatim in the source text."""
    bad = []
    def walk(n, path=""):
        if isinstance(n, dict):
            if n.get("evidence") and n["evidence"] not in source: bad.append(path)
            for k, v in n.items(): walk(v, f"{path}.{k}")
    walk(node)
    return bad

def to_scoring(x):
    g = lambda k: x[k]["value"]
    return {"licence_held_by_bidder": g("licence_held_by_bidder") is True,
            "wsib_and_insurance": bool(g("wsib_clearance_stated")) and (g("liability_insurance_cad") or 0) >= 5_000_000,
            "installs": g("qualifying_installs") or 0, "window_unclear": x["qualifying_installs"]["window_unclear"],
            "price": g("total_price_cad"), "weeks": g("completion_weeks"),
            "panel_yrs": g("panel_warranty_years") or 0, "work_yrs": g("workmanship_warranty_years") or 0,
            "lead": x["team"]["named_project_lead"]["value"], "crew": x["team"]["crew_size"]["value"] is not None,
            "safety": x["team"]["safety_plan"]["value"], "monitoring": x["team"]["monitoring_plan"]["value"],
            "injection": bool(x["suspicious_text"])}

out = {}
for f in sorted(pathlib.Path("samples").glob("*.txt")):
    text = f.read_text(); data = extract(text)
    bad = evidence_ok(data, text)
    if bad: print(f"{f.stem}: FLAGGED, quotes not found in source: {bad}")
    out[f.stem] = to_scoring(data)
json.dump(out, open("extractions.json", "w"), indent=2)
print("Wrote extractions.json. Now run: python score.py")
