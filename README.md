# Sloperator

A tree-walking interpreter for SlopLang, written in Python.

## Run

```bash
uv run sloperator.py examples/fib.slop      # run a program
uv run sloperator.py --check file.slop      # parse only; exits 1 on a syntax error
uv run playground/server.py                 # web playground at http://localhost:8080
```

## Validate

```bash
uv run pytest                # tests
uv run ruff format --check   # formatting
uv run ruff check            # linting
uv run ty check              # type checking
```

## Language

[`docs/spec.md`](docs/spec.md) is the single source of truth: words, values,
variables, control flow, functions, built-ins, operators, the grammar, and
error formats. This README deliberately does not restate them.

Runnable programs live in [`examples/`](examples/).

## Layout

| Path                    | What it is                            |
| ----------------------- | ------------------------------------- |
| `sloperator.py`         | Command-line entrypoint               |
| `sloperator/lexer/`     | Source text to tokens                 |
| `sloperator/parser/`    | Tokens to AST                         |
| `sloperator/evaluator/` | Values, environments, the interpreter |
| `sloperator/runner.py`  | Source through all three stages       |
| `docs/spec.md`          | The language specification            |
| `examples/`, `tests/`   | Example programs, pytest suite        |
| `playground/`           | Web server and editor page            |
