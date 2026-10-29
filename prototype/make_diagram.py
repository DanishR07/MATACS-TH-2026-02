import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

COL = {"rule": "#cfe2ff", "ai": "#ffd8a8", "human": "#c3f0ca"}
EDGE = {"rule": "#1c5fb8", "ai": "#d9730d", "human": "#2b8a3e"}
steps = [
 ("1  Upload PDFs +\nchoose category", "rule", (0,0)),
 ("2  Load criteria\n(frozen version ID)", "rule", (1,0)),
 ("3  Extract text\n(OCR if scanned)", "rule", (2,0)),
 ("4  Injection scan; mark\ntext as untrusted data", "rule", (3,0)),
 ("5  AI EXTRACTION\nfacts + evidence quotes\n(no scoring, no ranking)", "ai", (3,1)),
 ("6  Validate: quote exists,\ntypes OK, missing = null", "rule", (2,1)),
 ("7  Mandatory gate\npass/fail -> ineligible\n+ reason", "rule", (1,1)),
 ("8  HUMAN CHECK 1\nconfirm flags, gaps,\nineligibles; fix values", "human", (0,1)),
 ("9  Score weighted criteria\n(fixed formulas, code)", "rule", (0,2)),
 ("10  Rank + tie-break;\nincomplete bids held", "rule", (1,2)),
 ("11  AI EXPLANATION\nplain-English reason\nfrom the numbers only", "ai", (2,2)),
 ("12  HUMAN CHECK 2\nreview, override with\nreason, decide award", "human", (3,2)),
]
fig, ax = plt.subplots(figsize=(16, 9.5)); ax.set_xlim(0, 16); ax.set_ylim(0, 9.5); ax.axis("off")
ax.text(8, 9.15, "AI Proposal Triage: upload to ranked output (MATACS-TH-2026-02)", ha="center", fontsize=17, weight="bold")
w, h = 3.2, 1.5
pos = {}
for i, (t, kind, (c, r)) in enumerate(steps):
    x = 0.7 + c * 3.85; y = 7.0 - r * 2.6
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=COL[kind], ec=EDGE[kind], lw=2.2))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=10.5, weight="bold" if kind != "rule" else "normal")
    pos[i] = (x, y)
def arrow(a, b, side):
    (xa, ya), (xb, yb) = pos[a], pos[b]
    if side == "r": s, e = (xa + w, ya + h/2), (xb, yb + h/2)
    elif side == "l": s, e = (xa, ya + h/2), (xb + w, yb + h/2)
    else: s, e = (xa + w/2, ya), (xb + w/2, yb + h)
    ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="-|>", lw=2, color="#333"))
for a in (0,1,2): arrow(a, a+1, "r")
arrow(3, 4, "d")
for a in (4,5,6): arrow(a, a+1, "l")
arrow(7, 8, "d")
for a in (8,9,10): arrow(a, a+1, "r")
ax.text(pos[6][0] + w/2, pos[6][1] - 0.32, "ineligible bids stay visible, with reason", ha="center", fontsize=9, style="italic", color="#a61e4d")
ax.text(pos[3][0] + w/2, pos[3][1] + h + 0.2, "flag: suspicious instruction -> reviewer", ha="center", fontsize=9, style="italic", color="#a61e4d")
ax.text(pos[5][0] + w/2, pos[5][1] - 0.32, "failed validation -> flagged, never guessed", ha="center", fontsize=9, style="italic", color="#a61e4d")
ax.add_patch(FancyBboxPatch((0.7, 0.75), 14.6, 0.85, boxstyle="round,pad=0.05", fc="#f1f3f5", ec="#495057", lw=2))
ax.text(8, 1.17, "AUDIT LOG (append-only, every step): criteria version | prompt version | model ID | file hash | raw AI output | validated values | scores | flags | human edits + reasons | final decision",
        ha="center", va="center", fontsize=9.6)
for i, (k, lab) in enumerate([("rule", "Rule / plain code"), ("ai", "AI step"), ("human", "Human checkpoint")]):
    x = 3.3 + i * 3.6
    ax.add_patch(FancyBboxPatch((x, 0.15), 0.5, 0.35, boxstyle="round,pad=0.02", fc=COL[k], ec=EDGE[k], lw=2))
    ax.text(x + 0.65, 0.33, lab, va="center", fontsize=11)
plt.savefig("../diagram/flow.png", dpi=140, bbox_inches="tight", facecolor="white")
