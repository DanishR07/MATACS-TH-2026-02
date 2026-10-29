# Prototype (optional, extra credit)

| File | Purpose |
|---|---|
| `score.py` | Deterministic engine: mandatory gate, flags, weighted scoring, ranking. Run `python score.py` (no packages needed). Output matches `../ranking.json`. |
| `criteria.json` | What an admin would set for the category (weights, budget ceiling, 16-week limit). Nothing is hard-coded in the scorer. |
| `extractions.json` | Validated values, as the extraction step would produce them (numbers and yes/no only, no proposal text). |
| `extract.py` | Runs the extraction prompt from `../PROMPTS.md` on local files in `samples/`, checks each evidence quote exists in the source, and writes `extractions.json`. |
| `make_diagram.py` | Script that draws `../diagram/flow.png`. |
| `.env.example` | Template for the API key. The real `.env` is git-ignored and never committed. |

`samples/` is git-ignored on purpose: the brief says not to copy proposal text into the repository.
`extract.py` was syntax-checked but not run against the live API, since no key is stored in the repository.
