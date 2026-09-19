# Feature request

This is the raw intent, as it arrived from Finance. Paste it after `/speckit-specify`
in the Copilot chat panel.

---

> Finance spends two days a month checking expense submissions against the travel
> policy by hand. We want a command line tool they can run against a submitted
> expense file that tells them which lines break policy and why. It needs to handle
> the per diem caps, the receipt rule, and expenses that come in euros or pounds.
> Finance wants to stop arguing about whether a rule was applied consistently.
>
> Use the short name expense-policy-validator for this feature.

---

The last line isn't part of Finance's request. `/speckit-specify` makes up its own
short name for the feature folder, and without that line it might choose something
like `expense-validator`. Naming it keeps the folder at
`specs/001-expense-policy-validator/`, which is the path the README, the recovery
commands and the later demos all use.

## What to notice before running it

This is a realistic request, and it's longer than the one-shot prompt in demo 01, but
it still doesn't say what the per-diem caps are, whether they apply per day or per
trip, what counts as a receipt-worthy expense, or which exchange rate to use.

The difference is what happens next. The prompt-driven approach guessed. The
specification step marks what it can't resolve with `[NEEDS CLARIFICATION]` and
records the defaults it chose under Assumptions, so the guesses are visible and
reviewable instead of buried in code.
