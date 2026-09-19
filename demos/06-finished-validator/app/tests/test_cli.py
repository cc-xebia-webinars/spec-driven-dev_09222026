"""The command line contract.

Covers FR-008, FR-009 and FR-010, plus SC-004. Exit codes were decided during
clarification and written down before any of this existed, which is why they can
be asserted rather than discovered.
"""

from __future__ import annotations

import json

from expense_validator.cli import EXIT_MALFORMED, EXIT_OK, EXIT_VIOLATIONS, main


def run(policy_path, samples_dir, name, fmt="text"):
    return main(
        [
            "--policy", str(policy_path),
            "--submission", str(samples_dir / f"{name}.json"),
            "--format", fmt,
        ]
    )


def test_fr009_clean_submission_exits_zero(policy_path, samples_dir, capsys):
    assert run(policy_path, samples_dir, "berlin-trip") == EXIT_OK
    assert "No policy violations found." in capsys.readouterr().out


def test_fr009_violations_exit_one(policy_path, samples_dir):
    assert run(policy_path, samples_dir, "over-cap-meal") == EXIT_VIOLATIONS


def test_fr009_malformed_input_exits_two(policy_path, tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text('{"submission_id": "X"}', encoding="utf-8")
    code = main(["--policy", str(policy_path), "--submission", str(bad)])
    assert code == EXIT_MALFORMED
    assert "error:" in capsys.readouterr().err


def test_fr009_unsupported_currency_exits_two(policy_path, tmp_path, capsys):
    bad = tmp_path / "chf.json"
    bad.write_text(
        json.dumps(
            {
                "submission_id": "EXP-CHF",
                "traveller": "T",
                "trip_start": "2026-03-09",
                "trip_end": "2026-03-10",
                "city_tier": "2",
                "line_items": [
                    {"date": "2026-03-09", "category": "meal", "amount": "20.00",
                     "currency": "CHF", "receipt": "R-1", "description": "x"}
                ],
            }
        ),
        encoding="utf-8",
    )
    assert main(["--policy", str(policy_path), "--submission", str(bad)]) == EXIT_MALFORMED


def five_violation_submission(tmp_path):
    """One submission that breaks policy five separate ways.

    Two over-cap meals, one partial-day meal over the prorated cap, one missing
    receipt, and one line dated outside the trip. A validator that stops at the
    first problem reports one of these; FR-008 requires all five.
    """
    path = tmp_path / "five.json"
    path.write_text(
        json.dumps(
            {
                "submission_id": "EXP-FIVE",
                "traveller": "T",
                "trip_start": "2026-03-09",
                "trip_end": "2026-03-12",
                "city_tier": "2",
                "line_items": [
                    {"date": "2026-03-09", "category": "meal", "amount": "50.00",
                     "currency": "USD", "receipt": None, "description": "partial day"},
                    {"date": "2026-03-10", "category": "meal", "amount": "72.00",
                     "currency": "USD", "receipt": None, "description": "over cap"},
                    {"date": "2026-03-11", "category": "meal", "amount": "65.00",
                     "currency": "USD", "receipt": None, "description": "over cap"},
                    {"date": "2026-03-11", "category": "transport", "amount": "120.00",
                     "currency": "USD", "receipt": None, "description": "no receipt"},
                    {"date": "2026-03-20", "category": "transport", "amount": "10.00",
                     "currency": "USD", "receipt": None, "description": "after trip"},
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_fr008_every_violation_is_reported_in_one_pass(policy_path, tmp_path, capsys):
    code = main(
        ["--policy", str(policy_path),
         "--submission", str(five_violation_submission(tmp_path)),
         "--format", "json"]
    )
    payload = json.loads(capsys.readouterr().out)
    assert code == EXIT_VIOLATIONS
    rule_ids = sorted(v["rule_id"] for v in payload["violations"])
    assert rule_ids == [
        "date-outside-trip",
        "per-diem-cap",
        "per-diem-cap",
        "per-diem-cap",
        "receipt-required",
    ]


def test_sc004_five_distinct_violations_all_appear_in_the_text_report(
    policy_path, tmp_path, capsys
):
    main(["--policy", str(policy_path),
          "--submission", str(five_violation_submission(tmp_path))])
    out = capsys.readouterr().out
    assert "5 violations found:" in out
    assert out.count("\n  [") == 5


def test_fr010_each_violation_names_its_rule_and_limit(policy_path, samples_dir, capsys):
    run(policy_path, samples_dir, "over-cap-meal", fmt="json")
    payload = json.loads(capsys.readouterr().out)
    v = payload["violations"][0]
    assert v["rule_id"] == "per-diem-cap"
    assert v["amount_usd"] == "72.00"
    assert v["limit_usd"] == "60.00"
    assert "exceeds" in v["message"]


def test_sc001_text_report_shows_the_rule_id_for_every_violation(
    policy_path, samples_dir, capsys
):
    run(policy_path, samples_dir, "over-cap-meal")
    out = capsys.readouterr().out
    assert "[per-diem-cap]" in out
    assert "Approval required:" in out
