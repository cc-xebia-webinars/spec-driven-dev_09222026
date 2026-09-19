# Clarification answers

`/speckit-clarify` asks up to five questions, one at a time. Each comes with a
recommended option and a short explanation of why it matters. These are the answers
Finance gave. The wording of the questions varies from run to run, so match on the
topic rather than the exact text.

## The expected five

1. **Which exchange rate applies?**
   The corporate monthly rate in force on the transaction date, supplied in the policy
   data file. Rates are not fetched at runtime.

2. **Are per-diem caps per day or per trip?**
   Per travel day. The first and last day of a trip are prorated to 75 percent of the
   daily cap.

3. **Is a missing receipt above the threshold blocking or a warning?**
   Blocking. The submission does not pass.

4. **Where do the approval thresholds come from?**
   The policy data file, never hard-coded. The tiers are 500 USD and 2,500 USD.

5. **How should results be reported?**
   Every violation in one pass. Exit 0 for clean, 1 for violations found, 2 for
   malformed input.

## Spares, in case a different question comes up

- **What is the receipt threshold?** 75 USD.
- **What if a line is dated outside the trip?** Report it as a violation.
- **What about currencies other than euros and pounds?** Report malformed input rather
  than guessing a rate.

## If a question comes up that isn't covered here

Give any short, defensible answer and move on. The later demo folders start from the
committed reference spec, so nothing downstream depends on matching these exactly.
