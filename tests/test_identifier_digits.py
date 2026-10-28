"""Regression tests for issue #1: digits after the first character of a name."""

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_variable_name_with_trailing_digit():
    source = "slop score2 = 40✨\nscore2 = score2 + 2✨\nhallucinate(score2)✨\n"
    assert run(source) == "42\n"


def test_function_and_parameter_names_with_digits():
    source = "clanker add2(x1, y2) {\n  ship x1 + y2✨\n}\nhallucinate(add2(20, 22))✨\n"
    assert run(source) == "42\n"


def test_digits_may_appear_anywhere_after_first_character():
    source = "slop a1b2c3 = 1✨\nloadbearing _x9 = 2✨\nhallucinate(a1b2c3, _x9)✨\n"
    assert run(source) == "1 2\n"
