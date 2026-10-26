from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_equality_binds_looser_than_comparison():
    # `1 < 2 == ✅` must parse as `(1 < 2) == ✅`, not `1 < (2 == ✅)`.
    expr = only_expression("1 < 2 == ✅✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.right, Literal) and expr.right.value is True
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.LESS
    assert isinstance(expr.left.left, Literal) and expr.left.left.value == 1


def test_comparison_result_compared_for_equality():
    assert run("hallucinate(1 < 2 == ✅)✨") == "✅\n"


def test_equality_result_compared_with_number_is_false_not_an_error():
    # `(1 == 1) < 2` compares a boolean with a number. Equality never
    # coerces, so Python's `True < 2` must not leak through as `✅`.
    assert run("hallucinate(1 == 1 < 2)✨") == "❌\n"


def test_comparison_with_boolean_operand_is_a_runtime_error():
    result = run_source("hallucinate(✅ < 2)✨")
    assert result.exit_code == 1
    assert result.stderr == (
        "SlopLang runtime error at line 1: "
        "operands of '<' must be numbers, got boolean and number\n"
    )


def test_and_binds_looser_than_equality():
    # `✅ && 1 == 1` must parse as `✅ && (1 == 1)`.
    assert run("hallucinate(✅ && 1 == 1)✨") == "✅\n"


def test_boolean_and_number_equality_does_not_use_python_bool_coercion():
    # Python says `True == 1`; SlopLang says `❌`. Regression for `binary`
    # passing the raw `Expr` to `values_equal`, which compares by identity and
    # so answers every `==` except the trivial `a == a` with `❌`.
    assert run("slop one = 1✨\nhallucinate(✅ == one)✨") == "❌\n"
    assert run("slop two = 2✨\nhallucinate(two == 2)✨") == "✅\n"
    assert run("slop one = 1✨\nhallucinate(✅ != one)✨") == "✅\n"


def test_arithmetic_right_operand_is_evaluated():
    assert run("hallucinate(1 + 2 * 3)✨") == "7\n"
    assert run("hallucinate(10 - 2 - 3)✨") == "5\n"


def test_equality_chain_is_left_associative():
    # `1 == 1 == ✅` is `(1 == 1) == ✅`.
    assert run("hallucinate(1 == 1 == ✅)✨") == "✅\n"
