from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_tighter_than_addition():
    expr = only_expression("2 + 3 * 4✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.PLUS
    assert isinstance(expr.left, Literal) and expr.left.value == 2
    assert isinstance(expr.right, Binary) and expr.right.operator.type is TokenType.STAR


def test_multiplication_is_evaluated_before_addition():
    result = run_source("hallucinate(2 + 3 * 4)✨")
    assert result.stderr == ""
    assert result.stdout == "14\n"
