"""Turning a Result into something a person or a script can read.

Two formats, because the analyst reads the text one and the workflow system reads
the JSON one. Both carry the rule id, which is what SC-001 asks for.
"""

from __future__ import annotations

import json

from .rules import Result


def as_text(result: Result) -> str:
    lines = [f"Submission {result.submission_id}"]
    lines.append(f"Total: {result.total_usd} USD")
    lines.append(f"Approval required: {result.approval_tier.label}")
    lines.append("")

    if result.passed:
        lines.append("No policy violations found.")
        return "\n".join(lines)

    # Plural agreement matters more than it looks: this output gets pasted into
    # emails to the submitter, so "1 violations" reads as a bug in the tool.
    count = len(result.violations)
    noun = "violation" if count == 1 else "violations"
    lines.append(f"{count} {noun} found:")
    for v in result.violations:
        lines.append(f"  [{v.rule_id}] {v.message}")
    return "\n".join(lines)


def as_json(result: Result) -> str:
    payload = {
        "submission_id": result.submission_id,
        "total_usd": str(result.total_usd),
        "approval_tier": result.approval_tier.id,
        "approval_label": result.approval_tier.label,
        "passed": result.passed,
        "violations": [
            {
                "rule_id": v.rule_id,
                "date": str(v.line_item.date) if v.line_item else None,
                "category": v.line_item.category if v.line_item else None,
                "amount_usd": str(v.amount_usd) if v.amount_usd is not None else None,
                "limit_usd": str(v.limit_usd) if v.limit_usd is not None else None,
                "message": v.message,
            }
            for v in result.violations
        ],
    }
    return json.dumps(payload, indent=2)
