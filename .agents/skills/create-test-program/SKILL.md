---
name: create-test-program
description: Turn a SlopLang language feature into a runnable example plus an exact-output regression test. Use this skill whenever the user wants an example program under examples/, an exact-output test under tests/, a demo or showcase of a SlopLang feature, or a regression test for what a program prints — even if they don't say "skill", "example", or "test" explicitly.
---

# Create Test Program

Given a language feature, produce three artifacts that agree with each other:

1. a runnable example in `examples/<name>.slop`,
2. an exact-output test in `tests/test_example_outputs.py`,
3. passing validation.

The point of the pair is that the example becomes documentation of the feature and the
exact-output test pins its semantics, so a future change to the interpreter that quietly
alters what the feature prints fails loudly.

## Step 1 — Read the spec first

Read `docs/spec.md` before writing anything. It is the source of truth for syntax,
semantics, precedence, printing, and error text. Everything the example does must be
justified by the spec; do not invent syntax or rely on behavior you haven't confirmed.

Pay particular attention to:

- **Source text** — smart quotes `“ ”`, the `✨` terminator, the `—` comment, and the
  emoji literals `✅` / `❌`. Straight quotes, `;`, and `//` are errors.
- **Built-Ins** — `hallucinate` takes any number of arguments, separates them with a single
  space, and numbers print as base-10 digits, booleans as `✅`/`❌`, nil as `nil`.
- **Operators** — what the feature accepts and how it chains or binds.

If the user's request conflicts with the spec (for example, it assumes truthiness, which
SlopLang does not have), follow the spec and say so in your summary rather than writing a
program that can't run.

## Step 2 — Check what already exists

Look through `examples/` (for example with `ls examples/` and a quick grep for the
operator) before adding a file. Overlapping examples are fine when they isolate a distinct
bevel of the feature, but if an existing example already covers the request, extend the
skill's output only as far as the user asked — mention the overlap instead of silently
duplicating.

Pick a short kebab-or-single-word stem that names the feature (`equality.slop`,
`string-addition.slop`), matching the existing filenames.

## Step 3 — Write the example

Keep it small and focused: a title comment in the same em-dash style the other examples
use, then one statement per line demonstrating the feature. Every statement ends with `✨`.

Confirm each expected output by actually running the interpreter rather than reasoning
about it. While iterating, the quickest check is:

```bash
uv run sloperator.py examples/<name>.slop
```

`examples/` files must run cleanly — `tests/test_examples.py` runs every one of them and
requires exit code 0, empty stderr, and non-empty stdout. An example that errors is not
an example; if the feature's interesting case is an error, cover the error in the matching
`tests/test_*.py` file instead (see `tests/test_errors.py` for the exact diagnostic format).

## Step 4 — Add the exact-output test

Add the test to `tests/test_example_outputs.py`, following the shape already in that file:

```python
def test_<name>_example_prints_expected_output():
    assert run(EXAMPLE["<name>"]) == "line one\nline two\n"
```

Use the module's existing `EXAMPLE` map and `run` helper so the test stays consistent with
its siblings. Assert the **whole** stdout as one string, including trailing newlines, and
for an order-sensitive program keep the literal in program order — exact-output tests only
catch regressions if the expected text is byte-for-byte what the interpreter prints.

If `tests/test_example_outputs.py` does not exist yet, create it with:

```python
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
```

## Step 5 — Validate

Run the project's validate skill (`.agents/skills/validate/SKILL.md`) from the project
root. It runs the tests, the formatting check, the linter, and `ty check`. Both new checks
matter here: `pytest` proves the exact-output assertion holds now, and the formatting and
type checks keep the new test file consistent with the rest of the tree.

## Step 6 — Report

Summarize:

- the feature from the spec that the example demonstrates,
- the example file and the exact stdout it produces,
- the test added, and that the full suite passes.

Mention any place where the spec forced a different program than the one the user
described, and why.
