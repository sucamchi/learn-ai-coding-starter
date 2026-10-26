# AGENTS.md

Sloperator: a tree-walking interpreter for SlopLang (Python 3.13, `uv`). No CI.

## Project layout

Pipeline is three stages, wired by `runner.py` (`tokenize` → `parse` → `Interpreter`):

- `sloperator/lexer/` → `sloperator/parser/` → `sloperator/evaluator/` — each importable on its own.
- `sloperator/runner.py` — `run_source(source) -> RunResult`, the test seam: captures stdout
  in a `StringIO` and returns `(stdout, stderr, exit_code)` instead of printing. Prefer it
  over invoking the CLI in tests.
- `sloperator.py` — CLI entry point: `uv run sloperator.py [--check] <file.slop>` (repo root only).
- `tests/` — pytest suite. `examples/*.slop` — runnable sample programs.
- `playground/server.py` — local web playground on http://localhost:8080 (`uv run playground/server.py`).

## Validate

Always format after any code change — it is part of the normal workflow, not an optional
final step:

```bash
uv run ruff format
```

Run it once you finish a batch of edits, before anything else, and especially before you
report back. If it rewrites files, that is expected; re-run `ruff format --check` to confirm
the tree is clean. Then run the rest:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

All four are expected to pass on a clean tree. `ty check` is not in the `validate`
skill or the README's list, but `pyproject.toml` declares `ty` as a dev dependency
and it does catch real errors — run it too.

Single test: `uv run pytest tests/test_parser.py::test_calls_chain -q`

Comparison/equality tests: `uv run pytest tests/test_comparisons.py -q` (add new `==`, `!=`,
`<`, `>`, and precedence cases here).

## Add a regression test when...

- you fix a bug: reproduce it first, asserting the current wrong output, then make it pass.
- you change parser output, error text, or exit codes — `tests/test_errors.py` asserts exact
  strings via `f"SlopLang {kind} error at line {n}: {message}"`, so update or extend it.
- you add a language feature: cover success and failure paths in the matching
  `tests/test_lexer.py` / `test_parser.py` / `test_evaluator.py`.
- you add a file to `examples/`: `tests/test_examples.py` runs **every** `examples/*.slop` and
  requires empty stderr, exit code 0, and non-empty stdout.

## Language behavior

`docs/spec.md` is the source of truth for SlopLang syntax, semantics, error text, and exit
codes. Check it before "fixing" behavior that looks wrong.
