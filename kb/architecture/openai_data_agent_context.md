# OpenAI Data Agent Context Design

_Source: OpenAI internal data-agent writeup (Jan 2026). Compiled by Gashaw (Intelligence Officer)._

## Six-Layer Context Architecture

OpenAI's production data agent loads context in six layers with strict priority and
eviction rules. Higher-numbered layers are loaded later and evicted first under token
pressure.

| Layer | Name | Content | Load policy |
|-------|------|---------|-------------|
| 1 | Schema & Metadata | All table schemas, column types, indexes, relationships | Session start — never evicted |
| 2 | Institutional Knowledge | Authoritative table registry, data quality notes, owner teams | Session start — never evicted |
| 3 | Interaction Memory | Corrections from previous queries, resolved failure patterns | Session start — refreshed per session |
| 4 | Query Patterns | Successful SQL / aggregation pipeline templates from prior runs | Loaded on first query; evicted if token budget exceeded |
| 5 | Codex Table Enrichment | Semantic summaries for tables with > 100 columns | Loaded on demand; evicted first |
| 6 | Closed-Loop Self-Correction | Retry context: original query + error + retrieved correction | Injected only during retry; cleared after success |

## Layer-by-Layer Notes

**Layer 1 — Schema & Metadata**
Injected verbatim: CREATE TABLE statements, foreign key declarations, index types.
For multi-database agents: one schema block per engine (PostgreSQL, MongoDB, SQLite,
DuckDB). Never removed during a session — the agent cannot answer any query without it.

**Layer 2 — Institutional Knowledge**
Answers "which table is authoritative for X?" and "what does field Y mean in business
terms?". Prevents the agent from querying stale pre-aggregated tables when live data
exists (e.g. `business.stars` vs `reviews.stars` in Yelp).

**Layer 3 — Interaction Memory**
The only layer that persists across sessions. Stored as structured logs (JSONL).
Contains: query that failed, root cause, fix applied, confidence score. Agent loads
the top-N highest-confidence corrections matching the current query type.

**Layer 4 — Query Patterns**
Templates from past successful runs. Reduces LLM call latency by pre-filling known-good
JOIN structures and aggregation skeletons. Evicted before Layers 1–3 under pressure.

**Layer 5 — Codex Enrichment**
Auto-generated column-level summaries for wide tables. Not used for DAB datasets
(all tables < 50 columns). Placeholder in Oracle Forge context builder.

**Layer 6 — Self-Correction Loop**
On tool call failure: inject (original query + error message + closest matching
correction from Layer 3) and retry. Max 3 retries. On retry success, append the
resolution to Layer 3 for future sessions.

## Minimum Viable Implementation (Oracle Forge)

Three layers are sufficient for DAB pass@1 > 50 %:

| OpenAI Layer | Oracle Forge file |
|-------------|------------------|
| Layer 1 (schema) | `kb/domain/databases/[db]_schemas.md` |
| Layer 2 (institutional) | `kb/domain/domain_terms/`, `kb/domain/joins/join_key_mappings.md` |
| Layer 3 (corrections) | `kb/corrections/failure_log.md`, `kb/corrections/resolved_patterns.md` |

Layers 4–6 are implemented as stubs; Layer 6 is partially active (up to 3 retries in
`agent/main.py`).

## Critical Design Principle

Layers 1 and 2 must be injected **before** the LLM receives the user query. If schema
or institutional knowledge arrives after the question, the model generates a query plan
based on hallucinated schema and the correction loop cannot recover it in ≤ 3 retries.

---

## Injection Test

**Test query:** In the OpenAI six-layer context architecture, which layer contains
corrections from previous queries and how does it differ from the query patterns layer?

**Expected answer:** Layer 3 (Interaction Memory) contains corrections from previous
queries — specifically failed queries, their root causes, and the fixes applied. It
persists across sessions. Layer 4 (Query Patterns) contains successful SQL/pipeline
templates from prior runs. Layer 3 is about recovering from failures; Layer 4 is about
reusing successes. Layer 3 is loaded at session start; Layer 4 is evicted first under
token pressure.
