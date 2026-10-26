# AGENTS.md — parser

Conventions for `sloperator/parser/`.

## One method per grammar rule

Each method in `Parser` corresponds to exactly one rule of the grammar. Name the
method after the rule, and shape the method like the rule:

- A rule with alternatives (e.g. `statement: if_stmt | while_stmt | ...`) picks a
  branch inside its own method; the branches are separate methods only when they
  are rules themselves.
- A rule with a repetition (`factor: unary (("*" | "/") unary)*`) is a single
  method holding the loop. Do **not** split the loop into a separate `*_tail`
  helper that takes the already-parsed left operand — that breaks the
  one-method-per-rule mapping and hides the rule's shape.
- Don't fold two rules into one method to save code; precedence levels each get
  their own method.

## Syntax errors describe what was found

Every syntax error says what the parser expected **and** what it actually found.
Build them with `self.error(token, message)`, which appends `, found '<lexeme>'`
(or `, but reached end of file`); never raise a bare
`SlopSyntaxError` without the found-token context unless the message already
names the offending construct (e.g. `duplicate parameter name 'x'`).

```python
# good
raise self.error(self.peek(), "expected a variable name after 'slop'")
# -> "SlopLang syntax error at line 3: expected a variable name after 'slop', found '✨'"

# bad
raise SlopSyntaxError(line, "syntax error")
```
