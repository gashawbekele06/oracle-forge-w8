"""Plain-language formatting of `run_agent` results for CLI and Streamlit (no traces / raw JSON dumps)."""

from __future__ import annotations

from typing import Any, Dict, List


def format_answer_plain(result: dict) -> str:
    """Human-readable answer only — never raw trace, SQL, or large JSON dumps."""
    ans: Any = result.get("answer")
    if ans is None:
        err = result.get("error") or result.get("error_summary")
        if err:
            if isinstance(err, list):
                return "Could not complete that question: " + "; ".join(str(x) for x in err[:3])
            return f"Could not complete that question: {err}"
        return "No answer returned."

    if isinstance(ans, dict) and "metrics" in ans and "records" in ans:
        records = ans.get("records") or []
        metrics = ans.get("metrics") or {}
        if metrics and len(metrics) == 1:
            return str(next(iter(metrics.values())))
        if metrics:
            return "\n".join(f"{k}: {v}" for k, v in metrics.items())
        if len(records) == 1:
            row = records[0]
            if isinstance(row, dict):
                vals = list(row.values())
                if len(vals) == 1:
                    return str(vals[0])
                return ", ".join(str(v) for v in vals)
        if records:
            lines = []
            for row in records[:10]:
                if isinstance(row, dict):
                    lines.append(", ".join(f"{k}: {v}" for k, v in row.items()))
                else:
                    lines.append(str(row))
            return "\n".join(lines)
        return "(empty result)"

    if isinstance(ans, list):
        if not ans:
            return "(empty result)"
        if len(ans) == 2 and not isinstance(ans[0], (list, dict)):
            a0, a1 = ans[0], ans[1]
            if isinstance(a0, str) and isinstance(a1, (int, float)):
                return f"{a0}: average rating {a1}"
        lines: List[str] = []
        for i, item in enumerate(ans, start=1):
            if isinstance(item, (dict, list)):
                lines.append(f"{i}. {item!r}")
            else:
                lines.append(f"{i}. {item}")
        return "\n".join(lines)

    if isinstance(ans, dict):
        parts = [f"{k}: {v}" for k, v in list(ans.items())[:12]]
        return "\n".join(parts)

    return str(ans)
