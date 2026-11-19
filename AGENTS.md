# Agents

Follow CONTRIBUTING.md. Rules that matter most for an agent adding cases:

- A case is data, not code to improve. Never "clean up" a case program: a redundant
  `not (x == 2)` or an odd nesting may be the very thing it tests.
- Put it in `src/cc26_tests/cases/<group>/` by the *lowest* chapter it needs
  (var < if < loops < fun). Name it after what it checks; never `test_*` / `*_test`.
- Don't write `.out` from your head. Omit it (the oracle decides), or pin only what
  the oracle prints.
- Every loop must terminate; if it reads input, ship a `.in` with enough lines.
- Never copy files from cc26 in; the `cc26` provider reads them by path.
- Before finishing, run and show the output of:
  `uv run ruff format && uv run ruff check && uv run pytest src/cc26_tests/test_corpus.py`
- Harness changes (contract, env vars, Case fields) need a human decision: propose, don't apply.
