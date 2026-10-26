import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.stdout == ""
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
        ("!!!✅", "❌"),
    ],
)
def test_not_flips_booleans(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_spec_example():
    assert run("hallucinate(!✅, !❌, !!✅)✨") == "❌ ✅ ✅\n"


def test_not_binds_tighter_than_comparison():
    # `!1 == 2` must parse as `(!1) == 2`, so the number operand is rejected
    # rather than the result of `1 == 2` being flipped.
    assert fails("hallucinate(!1 == 2)✨") == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got number"
    )
    # `!` applies to the parenthesized comparison once grouped.
    assert run("hallucinate(!(1 == 2))✨") == "✅\n"


def test_not_binds_tighter_than_and():
    # `!✅ && ✅` is `(!✅) && ✅`, which is `❌`.
    assert run("hallucinate(!✅ && ✅)✨") == "❌\n"


@pytest.mark.parametrize(
    ("operand", "kind"),
    [
        ("1", "number"),
        ("“hi”", "string"),
        ("-1", "number"),
    ],
)
def test_not_rejects_non_booleans(operand: str, kind: str):
    assert fails(f"hallucinate(!{operand})✨") == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got {kind}"
    )


def test_not_in_condition():
    source = (
        "clanker check(flag) {\n"
        "    vibe !flag {\n"
        "        ship “off”✨\n"
        "    }\n"
        "    ship “on”✨\n"
        "}\n"
        "hallucinate(check(❌))✨\n"
        "hallucinate(check(✅))✨"
    )
    assert run(source) == "off\non\n"


def test_double_not_on_a_number_is_a_runtime_error():
    # `!` never coerces: `!!1` is not a boolean test on 1, and it is the inner
    # `!1` that fails.
    assert fails("hallucinate(!!1)✨") == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got number"
    )
