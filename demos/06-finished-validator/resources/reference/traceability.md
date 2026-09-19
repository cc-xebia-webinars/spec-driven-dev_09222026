# Traceability

Every requirement in the specification, the task that built it, the module where
it lives, and the tests that prove it. This table is **generated from the test
names**, not written by hand, which is why constitution principle II asks for the
requirement id in every test name - it makes this lookup mechanical.

| Requirement | Task | Module | Tests |
|---|---|---|---|
| FR-001 | T008 | `policy.py` | `test_approval_tiers.py::test_fr001_every_policy_value_is_read_from_the_file` |
| FR-002 | T009 | `rules.py` | `test_per_diem.py::test_fr002_tier_2_full_day_cap_is_sixty_usd`<br>`test_per_diem.py::test_fr002_meal_over_the_tier_cap_is_reported`<br>`test_per_diem.py::test_fr002_meal_under_the_tier_cap_is_not_reported`<br>`test_per_diem.py::test_fr002_non_meal_categories_are_not_capped` |
| FR-003 | T008 | `policy.py`, `models.py` | `test_per_diem.py::test_fr003_partial_day_cap_is_prorated_to_seventy_five_percent`<br>`test_per_diem.py::test_fr003_meal_on_a_partial_travel_day_uses_the_prorated_cap`<br>`test_per_diem.py::test_fr003_single_day_trip_prorates_once_not_twice` |
| FR-004 | T007 | `money.py` | `test_currency.py::test_fr004_converted_amount_is_compared_against_the_cap`<br>`test_currency.py::test_fr004_gbp_line_converts_and_stays_under_the_receipt_threshold`<br>`test_currency.py::test_fr004_total_is_summed_in_usd_after_conversion`<br>`test_money.py::test_fr004_rate_period_comes_from_the_transaction_date`<br>`test_money.py::test_fr004_usd_passes_through_untouched`<br>`test_money.py::test_fr004_eur_converts_at_the_march_rate`<br>`test_money.py::test_fr004_gbp_converts_at_the_march_rate` |
| FR-005 | T007, T021 | `money.py` | `test_money.py::test_fr005_unlisted_currency_is_malformed_input_not_a_guess`<br>`test_money.py::test_fr005_missing_rate_period_is_malformed_input` |
| FR-006 | T016 | `rules.py` | `test_receipts.py::test_fr006_threshold_comes_from_the_policy_file`<br>`test_receipts.py::test_fr006_missing_receipt_above_threshold_is_a_blocking_violation`<br>`test_receipts.py::test_fr006_missing_receipt_below_threshold_is_fine`<br>`test_receipts.py::test_fr006_receipt_present_above_threshold_is_fine`<br>`test_receipts.py::test_fr006_empty_receipt_string_counts_as_missing` |
| FR-007 | T008 | `policy.py` | `test_approval_tiers.py::test_fr007_small_total_needs_manager_approval`<br>`test_approval_tiers.py::test_fr007_total_above_five_hundred_needs_director_approval`<br>`test_approval_tiers.py::test_fr007_boundary_total_stays_in_the_lower_tier`<br>`test_approval_tiers.py::test_fr007_very_large_total_goes_to_finance`<br>`test_approval_tiers.py::test_fr007_empty_submission_reports_the_lowest_tier` |
| FR-008 | T011 | `rules.py` | `test_cli.py::test_fr008_every_violation_is_reported_in_one_pass` |
| FR-009 | T013 | `cli.py` | `test_cli.py::test_fr009_clean_submission_exits_zero`<br>`test_cli.py::test_fr009_violations_exit_one`<br>`test_cli.py::test_fr009_malformed_input_exits_two`<br>`test_cli.py::test_fr009_unsupported_currency_exits_two` |
| FR-010 | T012 | `report.py` | `test_cli.py::test_fr010_each_violation_names_its_rule_and_limit` |
| SC-001 | — | — | `test_cli.py::test_sc001_text_report_shows_the_rule_id_for_every_violation` |
| SC-002 | — | — | `test_approval_tiers.py::test_sc002_changing_a_threshold_needs_no_code_change` |
| SC-003 | — | — | **none** |
| SC-004 | — | — | `test_cli.py::test_sc004_five_distinct_violations_all_appear_in_the_text_report` |
| SC-005 | — | — | **none** |

**All 10 functional requirements have at least one test naming them.** Constitution principle II holds.

## Why the success criteria are thinner

Success criteria are technology-agnostic outcomes, so several of them can't be
asserted by a unit test at all. SC-005 is about Finance's working hours, and SC-003
is a performance budget better checked by timing a real run. That's expected: the
functional requirements are the testable contract, and the success criteria are
how you'd know the whole effort was worth it.
