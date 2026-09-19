# The one-shot prompt

This is the exact prompt that produced `app/src/prompt_built/validator.py`. It was pasted
into a chat session once, and the output was committed without edits.

---

> Write a Python command line tool that checks an expense submission against our
> travel policy. It should read a JSON file of expense line items and tell Finance
> which lines break policy. Handle the daily meal allowance, require receipts for
> large expenses, and support expenses in euros and pounds. Larger submissions need
> more approval.

---

## What this prompt leaves out

Read it again with the policy document open beside it. Every phrase below forced the
model to guess, and it guessed plausibly every time:

| The prompt says | The model had to decide | What it chose | What policy actually says |
|---|---|---|---|
| "the daily meal allowance" | how much | 50 USD, flat | 75, 60 or 45 by city tier |
| (nothing) | partial travel days | no special handling | first and last day at 75 percent |
| "large expenses" | the receipt threshold | 25 USD | 75 USD |
| "euros and pounds" | which exchange rate | 1.10 and 1.30, invented | Finance's monthly rate for the transaction date |
| "more approval" | the tiers | one threshold at 1,000 | two, at 500 and 2,500 |
| "which lines break policy" | one answer or all | the first one only | every violation in one pass |

None of these are bugs in the usual sense. The code does exactly what it was asked.
The problem is that nobody wrote down what was actually wanted.
