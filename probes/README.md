# `probes/` — Adversarial Probe Library

Adversarial test cases used to harden the Oracle Forge agent against known DAB failure modes.

## Files

| File | Description |
|------|-------------|
| `probes.md` | 21 documented probes covering all four DAB failure categories. Each probe has five required fields. |
| `test_probes.py` | Pytest runner that executes all probes against the live agent and reports pass/fail |

## Probe count and coverage

| DAB Failure Category | Probes | IDs |
|---------------------|--------|-----|
| Multi-database routing | 6 | M1–M6 |
| Ill-formatted key mismatch | 5 | J1–J5 |
| Unstructured text extraction | 4 | U1–U4 |
| Domain knowledge gap | 6 | D1–D6 |
| **Total** | **21** | |

## Required fields per probe

Every probe in `probes.md` contains:

1. **Query** — the natural language question
2. **Failure category** — one of the four DAB failure types
3. **Expected failure** — what the agent would get wrong without the fix
4. **Observed agent response** — what the agent actually returned before the fix
5. **Fix applied + post-fix score** — what changed in the agent/KB and the resulting pass@1

## How to run

```bash
# Requires Docker stack running (postgres, mongo, toolbox)
python eval/run_probes.py

# Or with pytest directly
python -m pytest probes/test_probes.py -v
```

Results are written to `eval/probe_results.json`.
