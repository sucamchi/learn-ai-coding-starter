import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“” + “slop”", "slop"),
        ("“slop” + “”", "slop"),
        ("“café” + “✨”", "café✨"),
        ("“” + “”", ""),
        ("“✨” + “✨”", "✨✨"),
        ("“café” + “” + “”", "café"),
    ],
)
def test_string_addition(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_spec_example():
    assert run("hallucinate(“café” + “✨”)✨") == "café✨\n"


def test_adding_an_empty_string_preserves_the_original():
    for original in ["slop", "café", "✨", "a b c"]:
        assert run(f"hallucinate(“{original}” + “”)✨") == f"{original}\n"
        assert run(f"hallucinate(“” + “{original}”)✨") == f"{original}\n"


def test_emoji_survives_concatenation_byte_for_byte():
    # Emoji are outside the BMP; make sure nothing mangles or double-counts them.
    assert run("hallucinate(“✨” + “café”)✨") == "✨café\n"


def test_concatenated_strings_can_be_compared():
    assert run("hallucinate(“slop” + “” == “slop”)✨") == "✅\n"
    assert run("hallucinate(“café” + “✨” == “café✨”)✨") == "✅\n"
