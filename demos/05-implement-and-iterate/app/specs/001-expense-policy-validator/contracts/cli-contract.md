# Contract: `expense-validate` command line interface

**Phase 1 output.** This contract is what callers depend on. Changing anything here
is a breaking change, not a tidy-up.

## Invocation

```
expense-validate --policy <path> --submission <path> [--format text|json]
```

| Option | Required | Default | Meaning |
|---|---|---|---|
| `--policy` | yes | — | Path to the policy JSON file |
| `--submission` | yes | — | Path to the submission JSON file |
| `--format` | no | `text` | `text` for a person, `json` for the workflow system |

## Exit codes (FR-009)

| Code | Condition | Stream used |
|---|---|---|
| 0 | Validation ran and found no violations | report on stdout |
| 1 | Validation ran and found one or more violations | report on stdout |
| 2 | Input could not be understood | message on stderr |

Exit 1 is a successful run that found problems. Exit 2 means no validation happened.
Callers that treat any non-zero code as a crash will misreport the common case, which
is why the two are distinct.

Errors go to stderr so that `--format json` output on stdout stays parseable even
when the run fails.

## Text output

```
Submission EXP-2026-0418
Total: 116.00 USD
Approval required: Manager approval

1 violation found:
  [per-diem-cap] 2026-03-10 meal of 72.00 USD exceeds the daily cap of 60.00 USD for city tier 2
```

Every violation line begins with its rule id in square brackets (SC-001). The count
line uses singular or plural correctly, because this output gets pasted into emails.

## JSON output

```json
{
  "submission_id": "EXP-2026-0418",
  "total_usd": "116.00",
  "approval_tier": "manager",
  "approval_label": "Manager approval",
  "passed": false,
  "violations": [
    {
      "rule_id": "per-diem-cap",
      "date": "2026-03-10",
      "category": "meal",
      "amount_usd": "72.00",
      "limit_usd": "60.00",
      "message": "2026-03-10 meal of 72.00 USD exceeds the daily cap of 60.00 USD for city tier 2"
    }
  ]
}
```

Monetary values are strings, for the same reason they are strings on input: a JSON
number would be a float by the time a consumer read it.

## Rule identifiers

| `rule_id` | Raised when |
|---|---|
| `per-diem-cap` | A meal line exceeds the daily or prorated cap for the tier |
| `receipt-required` | A line above the receipt threshold has no receipt reference |
| `date-outside-trip` | A line is dated outside the trip start and end |

New rules add identifiers. Existing identifiers do not change meaning.
