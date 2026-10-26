"""Exact expected stdout for each program in examples/."""

from pathlib import Path

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


EXAMPLE = {path.stem: path.read_text(encoding="utf-8") for path in EXAMPLES.glob("*.slop")}


def test_equality_example_prints_expected_output():
    # Equality never coerces: `1 == 1` is ✅, but a number and a string, and a
    # boolean and a number, are different types and so unequal.
    assert run(EXAMPLE["equality"]) == "✅\n❌\n❌\n"


def test_short_circuit_example_prints_expected_output():
    # `&&` and `||` bind looser than `==`, so each right side is a complete
    # comparison. Skipping it means `1 / 0` is never evaluated and so cannot
    # raise division by zero.
    assert run(EXAMPLE["short-circuit"]) == "❌\n✅\n"
