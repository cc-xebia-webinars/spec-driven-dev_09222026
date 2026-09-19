"""Expense validator produced from a single prompt.

This file is committed exactly as it came out of a one-shot prompting session. The
prompt that produced it is in `../resources/prompts/one-shot-prompt.md`. Nothing
here has been corrected, because the point of this demo is what the model assumed
when nobody told it otherwise.

Read the constants below against `../resources/acme-travel-policy.md` and notice that
every one of them is a reasonable guess and none of them is right.
"""

from __future__ import annotations

import json
import sys

# The prompt said "the daily meal allowance" without giving a number, so the model
# picked one. The real policy has three tiers: 75, 60 and 45.
DAILY_MEAL_CAP = 50.00

# The prompt said receipts are needed for "large expenses". The real threshold is 75.
RECEIPT_THRESHOLD = 25.00

# The prompt mentioned euros and pounds. These rates were invented; the real ones
# are published monthly by Finance and live in the policy data file.
EXCHANGE_RATES = {"USD": 1.0, "EUR": 1.10, "GBP": 1.30}

# The prompt said larger submissions need more approval. One threshold seemed
# enough. The real policy has two, at 500 and 2500.
APPROVAL_THRESHOLD = 1000.00


def convert(amount, currency):
    rate = EXCHANGE_RATES.get(currency)
    if rate is None:
        # Nothing in the prompt said what to do here, so it falls back to treating
        # the amount as dollars and carries on.
        rate = 1.0
    return round(amount * rate, 2)


def validate(submission):
    """Check a submission and return the first problem found.

    The prompt asked the tool to "tell them which lines break policy". The model
    read that as one answer per run and returns as soon as it finds something.
    """
    for item in submission.get("line_items", []):
        usd = convert(float(item["amount"]), item.get("currency", "USD"))

        if item.get("category") == "meal" and usd > DAILY_MEAL_CAP:
            return f"Meal on {item['date']} is over the {DAILY_MEAL_CAP} daily limit"

        if usd > RECEIPT_THRESHOLD and not item.get("receipt"):
            return f"Expense on {item['date']} needs a receipt"

    return None


def approval_for(submission):
    total = sum(
        convert(float(i["amount"]), i.get("currency", "USD"))
        for i in submission.get("line_items", [])
    )
    return "director" if total > APPROVAL_THRESHOLD else "manager"


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: validator.py <submission.json>")
        return 1

    with open(argv[0], encoding="utf-8") as fh:
        submission = json.load(fh)

    problem = validate(submission)
    if problem:
        print(problem)
        return 1

    print("Looks fine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
