# Claude Code Memory System

_Source: Claude Code architecture (March 2026). Compiled by Gashaw (Intelligence Officer)._

## Three-Layer Memory Architecture

Claude Code organises persistent knowledge across three distinct layers, each with a
different scope, size limit, and eviction policy.

### Layer 1 — MEMORY.md (session index)

- Single file at the repository root; never exceeds **500 lines**.
- Contains: project structure pointers, key file locations, architectural decisions,
  and one-line hooks to Layer 2 topic files.
- Loaded at agent session start and **kept in context for the entire session**.
- Rule: MEMORY.md is an index, not a store. Raw facts belong in Layer 2 files.

### Layer 2 — Topic Files (on-demand knowledge)

- One file per responsibility: `DATABASE_SCHEMA.md`, `JOIN_STRATEGY.md`,
  `API_CONTRACTS.md`, etc.
- Maximum **400 words per file**; single-topic only.
- Loaded **only when a MEMORY.md pointer is encountered** during a query — prevents
  context pollution with irrelevant knowledge.
- For Oracle Forge these map to: `kb/architecture/`, `kb/domain/`, `kb/corrections/`.

### Layer 3 — Session Transcripts (searchable history)

- Full interaction logs stored as `.jsonl` files (one record per tool call or message).
- Agent searches transcripts when encountering phrases like "we solved this before" or
  when a failure type matches a prior correction.
- **AutoDream consolidation**: every 10 sessions the agent compresses transcripts into
  Layer 2 topic files, discarding raw logs. Keeps Layer 3 bounded.

## Load Order for Oracle Forge

| Step | When | Files loaded |
|------|------|-------------|
| 1 | Session start (always) | `MEMORY.md`, `kb/domain/joins/join_key_mappings.md`, `kb/corrections/failure_log.md` |
| 2 | Query needs specific DB | `kb/domain/databases/[db_type]_schemas.md` |
| 3 | Join failure detected | `kb/domain/joins/cross_db_join_patterns.md`, `kb/corrections/failure_by_category.md` |
| 4 | Pattern not in Layer 2 | Search Layer 3 transcripts for prior resolution |

## Key Design Decisions

- **No embeddings / no RAG**: knowledge is loaded by rule, not retrieved by similarity.
  Deterministic injection eliminates hallucinated retrieval misses.
- **Size limits enforce quality**: a 400-word limit forces authors to write facts, not
  prose. Long documents are a signal the file should be split.
- **AutoDream prevents drift**: periodic consolidation keeps Layer 2 current without
  manual curation.

## Oracle Forge mapping

| Claude Code concept | Oracle Forge implementation |
|--------------------|-----------------------------|
| MEMORY.md (Layer 1) | `kb/README.md` + `kb/CHANGELOG.md` |
| Topic files (Layer 2) | All `.md` files under `kb/architecture/`, `kb/domain/`, `kb/corrections/` |
| Session transcripts (Layer 3) | `docs/driver_notes/runtime_corrections.jsonl`, `docs/driver_notes/agent_runtime_log.jsonl` |
| AutoDream consolidation | Weekly `kb/corrections/resolved_patterns.md` update |

---

## Injection Test

**Test query:** What are the three layers of the Claude Code memory system and what
does each layer store?

**Expected answer:** Layer 1 is MEMORY.md — a session-persistent index capped at
500 lines. Layer 2 is on-demand topic files (max 400 words each) loaded only when
referenced by MEMORY.md. Layer 3 is session transcripts stored as JSONL, searchable
for prior corrections, periodically consolidated into Layer 2 by AutoDream.
