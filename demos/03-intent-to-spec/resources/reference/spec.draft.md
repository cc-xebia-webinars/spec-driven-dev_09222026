# Feature Specification: Expense Policy Validator

**Feature Branch**: `001-expense-policy-validator`

**Created**: 2026-01-05

**Status**: Draft

**Input**: User description: "Finance spends two days a month checking expense submissions against the travel policy by hand. We want a command line tool they can run against a submitted expense file that tells them which lines break policy and why. It needs to handle the per diem caps, the receipt rule, and expenses that come in euros or pounds. Finance wants to stop arguing about whether a rule was applied consistently."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Check a submission against the meal per diem (Priority: P1)

A Finance analyst receives an expense submission for a trip and needs to know whether any meal line exceeds the daily allowance for that destination. They run the validator against the submission file and read the violations it reports.

**Why this priority**: Meal per diem is the rule that generates the most disputes and the most manual checking time. A tool that does only this is already worth running.

**Independent Test**: Can be fully tested by validating a submission containing meal lines above and below the tier cap, and confirming the tool reports exactly the lines that exceed it.

**Acceptance Scenarios**:

1. **Given** a Tier 2 destination with a 60 USD daily meal cap, **When** a meal line of 72 USD is validated, **Then** the tool reports a per-diem violation naming the cap and the amount.
2. **Given** a Tier 2 destination with a 60 USD daily meal cap, **When** a meal line of 48 USD is validated, **Then** the tool reports no violation for that line.
3. **Given** a trip whose first day is a partial travel day, **When** a meal line falls on that day, **Then** the tool applies the reduced cap for partial days.

---

### User Story 2 - Enforce the receipt rule (Priority: P2)

A Finance analyst needs to know which line items are missing a receipt that policy requires, so the submission can be returned to the submitter before any approval is sought.

**Why this priority**: Missing receipts are the most common reason a submission is returned. Catching them automatically removes a whole round trip, but the per-diem check is more valuable if only one ships.

**Independent Test**: Can be fully tested by validating a submission containing line items above and below the receipt threshold, with and without receipts attached.

**Acceptance Scenarios**:

1. **Given** a receipt threshold of 75 USD, **When** a 120 USD line item has no receipt, **Then** the tool reports a blocking receipt violation.
2. **Given** a receipt threshold of 75 USD, **When** a 40 USD line item has no receipt, **Then** the tool reports no violation for that line.
3. **Given** a 120 USD line item with a receipt reference present, **When** the submission is validated, **Then** the tool reports no receipt violation.

---

### User Story 3 - Handle foreign currency and approval routing (Priority: P3)

A Finance analyst validates a submission containing euro and pound expenses and needs those converted to US dollars before the caps are applied, and needs to know which approval tier the total falls into.

**Why this priority**: Foreign expenses are a minority of submissions, and approval routing is currently handled by a separate process. Valuable, but the submission can be checked without it.

**Independent Test**: Can be fully tested by validating a submission containing EUR and GBP line items and confirming both the converted amounts and the reported approval tier.

**Acceptance Scenarios**:

1. **Given** a EUR line item, **When** the submission is validated, **Then** the tool compares the converted US dollar amount against the cap.
2. **Given** a submission in a currency the policy does not list, **When** the submission is validated, **Then** the tool reports malformed input rather than guessing a rate.
3. **Given** a submission totalling 1,800 USD, **When** the submission is validated, **Then** the tool reports that director approval is required.

---

### Edge Cases

- What happens when a trip is a single day, making it both the first and last day? The prorated cap is applied once, not twice.
- What happens when a line item's transaction date falls outside the trip dates? The tool reports it as a violation rather than silently accepting it.
- What happens when the policy file lists no rate for the period in question?
- How does the system handle a submission with no line items? It passes with no violations and reports the lowest approval tier.
- What happens when an amount is negative? The tool reports malformed input.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read every policy value — tier caps, receipt threshold, proration rate, approval tiers, and exchange rates — from a policy data file supplied at runtime.
- **FR-002**: System MUST compare each meal line item against the daily meal cap for the destination tier recorded on the submission.
- **FR-003**: System MUST apply the meal cap [NEEDS CLARIFICATION: is the cap per travel day or across the whole trip, and how are partial travel days treated?]
- **FR-004**: System MUST convert line items denominated in EUR or GBP to US dollars before applying any cap, using [NEEDS CLARIFICATION: which exchange rate - transaction date, submission date, or a fixed corporate rate?]
- **FR-005**: System MUST report malformed input when a line item uses a currency the policy file does not list, rather than assuming a rate.
- **FR-006**: System MUST flag any line item above the receipt threshold that has no receipt reference [NEEDS CLARIFICATION: is a missing receipt blocking, or a warning the analyst can override?]
- **FR-007**: System MUST determine the required approval tier from the submission total using the thresholds in the policy file.
- **FR-008**: System MUST report every violation found in a single pass rather than stopping at the first.
- **FR-009**: System MUST exit with status 0 when no violations are found, 1 when violations are found, and 2 when the input is malformed.
- **FR-010**: Each reported violation MUST name the policy rule that produced it, the offending amount, and the limit that was exceeded.

### Key Entities *(include if feature involves data)*

- **ExpenseSubmission**: One employee's expenses for one trip. Carries the traveller, the trip start and end dates, the destination city tier, and a collection of line items.
- **LineItem**: A single claimed expense. Carries a date, a category, an amount, a currency, an optional receipt reference, and a description.
- **PolicyRule**: A single reimbursement constraint read from the policy file, such as a tier cap or the receipt threshold. Carries an identifier, a limit, and the text used when reporting a violation.
- **Violation**: One failed check. Carries the line item it refers to, the policy rule that failed, the offending amount, and the limit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every reported violation traces to exactly one named policy rule, so a reviewer can resolve a dispute without reading the source code.
- **SC-002**: Changing any policy number requires editing only the policy data file and its test, with no change to application code.
- **SC-003**: A submission of 100 line items is validated in under one second on a standard laptop.
- **SC-004**: A submission containing five distinct violations reports all five on a single run.
- **SC-005**: Finance reduces the time spent manually checking submissions from two days a month to under two hours.

## Assumptions

- Submissions arrive as a single structured file per trip. Batch validation across many submissions is out of scope for this version.
- The city tier is recorded on the submission rather than derived from the destination name, because the tier list changes independently of this tool.
- Exchange rates are supplied in the policy data file and maintained by Finance monthly. The tool does not fetch rates, which keeps it offline and deterministic.
- Only EUR and GBP are supported, matching current policy. Adding a currency is a policy file edit.
- Approval routing reports the required tier. Actually routing the submission for approval belongs to the existing workflow system and is out of scope.
- Approval tier thresholds are assumed to live in the policy data file alongside the other limits, on the same reasoning as the caps.
- The tool is assumed to report every violation in one pass rather than stopping at the first, since an analyst wants the whole picture before replying to the submitter.
