from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_assignment_in_nested_block_updates_nearest_binding():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨"""
    assert run(source) == "3\n1\n"


def test_assignment_in_block_inside_function_updates_function_local():
    source = """slop score = 1✨
clanker bump() {
    slop score = 2✨
    {
        score = 3✨
    }
    ship score✨
}
hallucinate(bump())✨
hallucinate(score)✨"""
    assert run(source) == "3\n1\n"
