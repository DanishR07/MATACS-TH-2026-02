# Write-up: MATACS-TH-2026-02

**Assumptions (stated rather than waiting for a reply)**
- "Last 5 years" is counted by calendar year, so 2021 onward. A bidder who says "since 2020" is counted as stated but flagged, because some installs may fall outside the window.
- Missing information is never guessed. A missing value scores 0 on that criterion and the proposal is flagged.
- Price and timeline are scored against the best *eligible* bid. Going over the budget or 16 weeks is flagged for a human, not silently scored.
- Team and approach is a four-item checklist (named lead, crew size, safety plan, monitoring plan), 25 points each.

## 1. AI vs. rules
**AI does two jobs only:** (a) read messy proposal text and fill a fixed form of facts, each with a supporting quote; (b) turn final numbers into a plain-English reason.

**Plain code does everything else:** loading criteria, the pass/fail gate, all score maths, ranking and logging.

*Why this line:* reading free text is what AI is good at. Maths, thresholds and ordering must be exact and identical every run, so they belong in code. The AI never sees the weights and never produces a score or rank, so a wrong or manipulated AI answer cannot directly change the result.

## 2. Consistency and explainability
- **Repeatable:** the model runs at temperature 0 with a pinned version and a strict JSON schema. Each extraction is cached by file hash + prompt version + model. Re-ranking reuses the cache, and scoring is pure code. So ranking the same proposals twice gives the same result.
- **Explainable:** every proposal has a score sheet. For each criterion it shows the extracted value, the quote it came from, the formula and the points earned. Clicking a rank opens that sheet, and the reason line is generated from those numbers.
- **Ties:** broken by higher experience score, then lower price.

## 3. Human in the loop
- **Checkpoint 1 (before scoring):** the reviewer sees flags, gaps and ineligible bids with reasons. They can correct an extracted value, with the quote shown beside it, and must give a reason.
- **Checkpoint 2 (after ranking):** the reviewer can reorder, exclude or restore a bid, again with a mandatory written reason. **The award is always a human decision.** The tool never awards anything.
- **Audit log (append-only):** who and when; criteria version; prompt version; model ID; file hash; raw AI output; validated values; flags; scores; every human edit with reason; the final decision.

## 4. Changing criteria
- Criteria are versioned. A run stores the version it used and old results are never overwritten.
- When an admin edits weights or criteria, existing results are labelled "scored under v1" and the reviewer sees a "criteria changed" banner.
- **Re-run:** if the new criteria use facts already extracted, only scoring is recomputed (instant, free). If a new criterion needs a new fact, only that extraction is re-run. The result is saved as a new run so the reviewer can compare old and new side by side.
- Changes to mandatory criteria can change eligibility, so they are highlighted. Once a human approves a ranking, that version is locked.

## 5. Risks and safeguards
| Risk | Safeguard |
|---|---|
| Wrong extraction | Every value needs a verbatim quote that code checks exists in the source text. Mismatches are flagged. Human checkpoint 1. |
| Made-up facts | The prompt allows "not stated" (null). Nulls score 0 and are flagged, never filled in. |
| Prompt injection / manipulation | Proposal text is treated as untrusted data. A scan flags instruction-like text. The AI output schema has no field for rank or score, and scoring is code. Flagged text is shown to the reviewer. |
| Bias | Scoring uses only stated facts and fixed formulas. Bidder names are masked during extraction and scoring. Overrides are logged. |
| Unfair relative scoring | Benchmarks use eligible bids only, so an ineligible cheap bid cannot distort the rest. |
| Cost | One extraction call per proposal, cached. Scoring is free. Page and size limits on uploads. |
| Bad PDFs / OCR errors | Low-confidence text or failed validation is flagged for a person. |
| Over-trust in the ranking | Humans decide. Flags and uncertainty are shown next to the rank. |

## Sample set results
- **A, rank 1 (94.8):** strongest experience, fast, competitive price, and the only complete team plan besides E.
- **E, rank 2 (82.2):** best warranty and monitoring, but fewer qualifying installs.
- **C, rank 3 (74.5):** eligible, but no safety or monitoring plan. It contains an embedded instruction aimed at automated reviewers. The instruction was ignored, so the score reflects the bid's real content. The bid is flagged so a person can decide whether it is a bidder integrity issue.
- **D, flagged (provisional 67.0):** no completion time, so timeline cannot be scored and the 16-week limit cannot be confirmed. Even with the best possible timeline it reaches about 82 and cannot overtake A. It is held for the reviewer to request clarification.
- **B, ineligible:** the licence would be held by a subcontractor "to be confirmed", not by the bidder. It fails a mandatory criterion, despite the lowest price and fastest timeline.

**Sensitivity check:** if C's experience were reduced to 7 installs, it would still sit above D's provisional score. If D were excluded, A's lead would only grow.
