# MATACS-TH-2026-02: AI Proposal Triage Design

| | |
|---|---|
| **Full name** | Danish Riasat |
| **Reference** | MATACS-TH-2026-02 |
| **Role** | Associate Software Developer |
| **Time actually spent** | About 1 hour 30 minutes: roughly 60 minutes on the design, write-up, prompts and ranking, and 30 minutes on the diagram, the optional prototype and a final review. |

## Summary
AI is used only to read messy proposal text into a fixed form, where every value must carry a word-for-word supporting quote, and to write a short plain-English reason from finished numbers. Plain code handles the mandatory pass/fail gate, the scoring formulas, the ranking and the audit log. A person reviews flags before scoring and makes the final award decision after ranking. Nothing written inside a proposal can change a score directly.

**Result on the sample set:** A ranked 1st, E 2nd, C 3rd (flagged), D flagged and held for clarification, B ineligible.

## Files
- [WRITEUP.md](WRITEUP.md): answers to the five questions (909 words)
- [diagram/flow.png](diagram/flow.png): process flow from upload to ranked output, showing AI steps, rule steps and human checkpoints
- [PROMPTS.md](PROMPTS.md): the extraction prompt and the reason-writer prompt, as they would be sent
- [ranking.json](ranking.json): expected ranking and scores for proposals A to E
- [prototype/](prototype/): optional scripts, including a scorer that reproduces the ranking (`python score.py`) and an extraction runner (`extract.py`)

## How I used AI tools
I used Claude (Anthropic) to help draft the design, write-up, prompts, diagram and prototype. I made the decisions about the design approach, reviewed every file, and checked the scores by recalculating them by hand and running `prototype/score.py`.

**Where I corrected the AI:** the first draft promised in the write-up that Proposal C's unclear "since 2020" experience window would be flagged for review, but the prototype never raised that flag, so the code did not match the document. I asked for a review of the draft against itself, found the mismatch, and had the scorer fixed so it now flags C's window. I also moved the diagram-drawing script out of `diagram/` so that folder holds a single image, as the brief requires.
