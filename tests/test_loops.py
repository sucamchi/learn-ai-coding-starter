from sloperator.runner import run_source

FALSE_FROM_THE_START = "ralph ❌ {\n    hallucinate(“never”)✨\n}"


def test_loop_with_false_condition_prints_nothing():
    result = run_source(FALSE_FROM_THE_START)
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
