---
name: create-and-validate
description: Create a SlopLang example plus its exact-output test, then validate the project. Use this skill whenever the user wants a new examples/*.slop program, an exact-output test for what a SlopLang program prints, or a change checked end to end with the project's test, format, lint, and type checks — including casual requests like "add an example for <feature>" or "make a slop program that prints X".
---

# Create and Validate

Two steps, in this order. This skill owns the ordering and nothing else; the
step-by-step detail lives in the two skills below, which are the source of truth.

## 1. Create the program

Load the `create-test-program` skill by ID and follow it exactly. It reads
`docs/spec.md`, writes a runnable example in `examples/`, and adds an
exact-output test to `tests/test_example_outputs.py`.

Do not paraphrase or work from memory of that workflow — load it and follow it,
so the example, the test, and the spec stay in agreement with each other and
with any later changes to those instructions. That skill also covers the
syntax traps that make hand-written SlopLang examples fail (smart quotes, the
`✨` terminator, no truthiness), so skipping it tends to produce a program that
does not run.

In this project, loading `create-test-program` may require approval because it
writes new files. If the load is rejected, stop and report that rather than
inventing the workflow from memory — writing an example without following the
skill defeats the purpose of the request.

## 2. Validate

Load the `validate` skill by ID and follow it. It runs the project's tests, the
formatting check, the linter, and `ty check`, in that order.

Run it only after step 1 has produced its files: validation is what proves the
new example and its exact-output assertion actually hold, so running it before
the files exist would only report a clean tree that says nothing about the new
work. If validation fails, fix the failure and run the whole skill again.

## Report

Summarize both stages in one reply:

- the example written and the exact stdout it produces,
- the test added,
- each check from `validate`, with pass or fail,
- anything the spec forced to differ from the user's request, and why.

Lead with failures if there are any.
