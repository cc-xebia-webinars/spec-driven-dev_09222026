"""Command line entry point.

The exit codes are part of the contract, decided during clarification and written
down as FR-009 before any of this was built. Callers depend on them, so changing
one is a breaking change rather than a tidy-up.
"""

from __future__ import annotations

import argparse
import sys

from .models import MalformedInput
from .policy import Policy
from .report import as_json, as_text
from .rules import load_submission, validate

EXIT_OK = 0
EXIT_VIOLATIONS = 1
EXIT_MALFORMED = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-validate",
        description="Check an expense submission against the travel policy.",
    )
    parser.add_argument("--policy", required=True, help="path to the policy JSON file")
    parser.add_argument("--submission", required=True, help="path to the submission JSON file")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="text for a person, json for the workflow system (default: text)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        policy = Policy.load(args.policy)
        submission = load_submission(args.submission)
        result = validate(submission, policy)
    except MalformedInput as exc:
        # Goes to stderr so that --format json stays machine-readable on stdout even
        # when the run fails.
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_MALFORMED

    print(as_json(result) if args.format == "json" else as_text(result))
    return EXIT_OK if result.passed else EXIT_VIOLATIONS


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
