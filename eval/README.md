# `eval/` — Evaluation Harness

Oracle Forge evaluation infrastructure for the DataAgentBench (DAB) benchmark.

## Files

| File | Purpose |
|------|---------|
| `run_dab_eval.py` | Main DAB benchmark runner — runs NL queries against the live agent and scores results |
| `dab_evaluator.py` | DAB evaluation logic: pass@1 computation, confidence intervals, structured output |
| `evaluator.py` | General evaluation harness with per-query tracing and result aggregation |
| `run_query.py` | Single-query runner for manual spot-checks |
| `run_probes.py` | Adversarial probe runner (against `probes/probes.md`) |
| `run_regression.py` | Regression suite runner (guards resolved failure patterns) |
| `run_yelp_baseline.py` | Yelp-specific baseline runner |
| `run_local_eval.py` | Local evaluation mode — does not require Docker/MCP Toolbox |

## Output files

| File | Format | Content |
|------|--------|---------|
| `score_log.jsonl` | JSON Lines | Aggregate run history — one record per evaluation run (baseline through latest) |
| `results.json` | JSON | **Per-query detail** for the most recent full DAB Yelp run: query id, question, pass/fail, trial accuracy, and full `query_trace` with tool calls, raw queries, and execution times |
| `sentinel_trace.jsonl` | JSON Lines | Per-query tool call traces from all runs — each line is one query execution with tool name, raw query, execution time, success/failure |
| `dab_results.json` | JSON | Per-query results for the PG+Mongo custom query set (54-query baseline) |
| `probe_results.json` | JSON | Adversarial probe results |
| `regression_results.json` | JSON | Regression suite results |
| `submission_results.json` | JSON | DAB benchmark submission summary |

## Reading the score log alongside per-query traces

`score_log.jsonl` records aggregate metrics per run (timestamp, dataset, pass@1, trial count).
Per-query detail with tool call traces lives in `results.json` (latest full run) and `sentinel_trace.jsonl` (all runs).

To correlate a score log entry with its per-query traces, match on `timestamp_utc`:

```python
import json

# Load aggregate log
with open("score_log.jsonl") as f:
    runs = [json.loads(line) for line in f if line.strip()]

# Load per-query results for the latest full run
with open("results.json") as f:
    per_query = json.load(f)

# Per-query record structure in results.json
for q in per_query["queries"]:
    print(q["id"], q["first_trial_correct"], len(q["trials"][0]["query_trace"]), "tool calls")
```

## How to rerun

Requirements: Docker stack running (`docker compose -f mcp/docker-compose.yml up -d postgres mongo toolbox`), `.env` configured with `MCP_BASE_URL=http://localhost:5000` and a valid LLM key (`GROQ_API_KEY` or `OPENROUTER_API_KEY`), and `DataAgentBench/` cloned at the repo root.

```bash
# Quick pass — 1 trial per query
DAB_TRIALS_PER_QUERY=1 python eval/run_dab_eval.py

# Full stress run — 50 trials per query (matches Apr 15 benchmark)
DAB_TRIALS_PER_QUERY=50 python eval/run_dab_eval.py

# Adversarial probes only
python eval/run_probes.py

# Regression suite only
python eval/run_regression.py
```

Results are appended to `score_log.jsonl` and written to `results.json` / `sentinel_trace.jsonl`.

## Baseline results

| Date | Dataset | Queries | Trials | pass@1 | Notes |
|------|---------|---------|--------|--------|-------|
| 2026-04-11 | PG+Mongo custom (54q) | 54 | 3 | 1.000 | First-run baseline on custom query set |
| 2026-04-15 | DAB Yelp (7q) | 7 | 2 | **0.857** | Best result on held-out DAB set (6/7 correct) |
| 2026-04-15 | DAB Yelp (7q) | 7 | 50 | 0.429 | Stress run (42.86% pass@1, 75.7% trial accuracy) |

Full run history in `score_log.jsonl`. Per-query traces in `results.json` and `sentinel_trace.jsonl`.
