from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Call, ExprStmt, Literal, Variable


def test_call_as_argument_to_another_call():
    (statement,) = parse(tokenize("hallucinate(add(1, 2))✨"))

    assert isinstance(statement, ExprStmt)
    outer = statement.expression
    assert isinstance(outer, Call)
    assert isinstance(outer.callee, Variable) and outer.callee.name.lexeme == "hallucinate"
    assert len(outer.arguments) == 1

    (inner,) = outer.arguments
    assert isinstance(inner, Call)
    assert isinstance(inner.callee, Variable) and inner.callee.name.lexeme == "add"
    assert len(inner.arguments) == 2
    first, second = inner.arguments
    assert isinstance(first, Literal) and first.value == 1
    assert isinstance(second, Literal) and second.value == 2
