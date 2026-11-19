# Contributing

## Add a test case (most contributions)

1. `src/cc26_tests/cases/<group>/<name>.py`, group = `var` | `if` | `loops` | `fun`
   (lowest chapter whose features it uses).
2. Name says what it checks: `while_nested_break_counter.py`, not `test3.py`.
   Never `test_*.py` / `*_test.py`.
3. Optional first-line comment if the name doesn't say what bug it catches.
4. Valid Python of that chapter: ints, bools, `input_int()`, `print(int)`. Must finish under
   CPython in well under a second.
5. `.in` if it reads input (one int per line). `.out` optional; if present it must match the oracle.
6. One feature per case. Found a bug with a fuzzer? Commit the (shrunk) program here.
7. Check: `uv run ruff format && uv run ruff check && uv run pytest src/cc26_tests/test_corpus.py` (same as CI, no compiler needed).

It is fine for a case to fail on your compiler — that is the point. It is not fine
for it to fail `test_corpus.py`.

## Add a provider

- A function `() -> Iterable[Case]`, registered in `PROVIDERS` (fuzzers: one `fuzz_<name>.py` each).
- Deterministic: same ids, same order, every run and every xdist worker. Seed randomness from `CT_SEED`.
- Ids `provider/group/name`, unique, no spaces.
- Cheap at import and collection; heavy work (oracle, compile) happens in the test.
- No network. Generated programs must terminate (bound every loop).
- Fuzzers are opt-in: do not add them to `DEFAULT`.

## Change the harness

- The contract (`COMPILER` template, `CC26`, exit codes, whitespace-split stdout) is shared by
  everyone. Changing it = say so in the PR title and README.
- Keep it stdlib + pytest. New dependency needs a reason in the PR.

## PRs

- Small, one topic. Commit style: `test: add while_nested_break_counter`, `feat: fuzz provider for arith`.
- Don't copy cc26 files in; reference them via the `cc26` provider.

## License

MIT, see LICENSE. Contributions are accepted under the same license.
