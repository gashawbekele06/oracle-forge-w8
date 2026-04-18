# `results/` — Benchmark Submission Evidence

This directory contains Oracle Forge's DataAgentBench (DAB) submission artefacts.

## DAB Pull Request

**PR link:** _(pending — to be submitted to [ucbepic/DataAgentBench](https://github.com/ucbepic/DataAgentBench))_

Required PR format:
- **Title:** `[Oracle Forge] - TRP1 FDE Programme, April 2026`
- **Body must include:**
  1. Agent name: Oracle Forge
  2. Backbone LLM model and version: `openai/gpt-4o-mini` via OpenRouter
  3. Dataset hints used: No
  4. Additional notes: Three-layer context injection (schema + domain + corrections); MCP Toolbox v0.30.0; PostgreSQL + MongoDB evaluated

## Files

| File | Description |
|------|-------------|
| `dab_submission.json` | Canonical DAB flat-list submission: 350 entries covering 7 Yelp queries × 50 trials each, in the required format (`dataset_name`, `query_id`, `run_number`, `agent_answer`) |

## Submission stats (April 15, 2026)

| Metric | Value |
|--------|-------|
| Dataset | DataAgentBench — Yelp |
| Queries | 7 |
| Trials per query | 50 |
| pass@1 | **0.4286** (42.86%) |
| Trial accuracy | 0.7571 (75.71%) |
| Best 2-trial run | **0.8571** (85.71%, 6/7 correct) |
| Databases active | PostgreSQL + MongoDB |

Full per-query traces with tool calls are in `eval/results.json`.
Score progression history is in `eval/score_log.jsonl`.

## How to rerun

```bash
# Ensure Docker stack is running
docker compose -f mcp/docker-compose.yml up -d postgres mongo toolbox

# Run 50-trial submission eval
DAB_TRIALS_PER_QUERY=50 python eval/run_dab_eval.py

# Results written to eval/results.json and appended to eval/score_log.jsonl
```
