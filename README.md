# cc26-tests

Shared end-to-end tests for our cc26 compilers. Assumption: **several people,
several compilers**, one shared corpus. The harness treats a compiler as a
black box: source in, x86 assembly out.

## Contract with a compiler

```
COMPILER="uv run compiler.py {src} -o {out}"   # default, = cc26 run_tests.py convention
```

Compiler prints the assembly to stdout instead? No `-o` needed:
`COMPILER="sh -c 'uv run compiler.py {src} > {out}'"`.

Split with `shlex.split`, run from pytest's working directory (your compiler repo root),
in a fresh `tmp_path` per test (xdist-safe).

- Compiler, gcc and binary must each exit 0, else the test fails with the stderr tail. Timeouts: 30 s compile, 10 s run. The assembly is linked with `gcc ... $CC26/support/runtime.c -Wl,-z,noexecstack`.
- `RUNTIME` replaces `$CC26/support/runtime.c` in that line: files and flags, `shlex`-split,
  relative to pytest's working directory. Needed for `tuples`, whose programs call
  `initialize` and `collect`, e.g. `RUNTIME="build/runtime-full.o cc26/support/runtime.c"`.
  `runtime-full.c` defines its own `print_int` and includes your `runtime.h`, so build
  that `.o` first: `gcc -c -w -I<dir with runtime.h> -Dprint_int=rt_print_int
  cc26/support/runtime-full.c -o build/runtime-full.o`.
- The `tuples` GC cases allocate about 1.5 MB in total, so a broken collector only fails them
  if your heap is smaller than that. Pass a small heap through `COMPILER`, e.g.
  `COMPILER="uv run compiler.py --heap-size 64 {src} -o {out}"`.
- `LINK` replaces that whole gcc line when one gcc call is not enough (e.g. the runtime
  must be compiled with its own flags first): a command with `{asm}` and `{exe}`,
  `shlex`-split like `COMPILER`, e.g. `LINK="./build.sh {asm} {exe}"`. Wins over `RUNTIME`.
- `CC26` (default `./cc26`) points at the course repo; it gives `runtime.c` and
  the cc26 cases. Missing → e2e tests skip with a reason, the cc26 provider yields nothing.
- Pass = the binary's stdout, split on whitespace, equals the expected output split
  the same way (as cc26 `run_tests.py` compares).

## Use from pytest

Install as a dev dependency (git or path source in `[tool.uv.sources]`), then either:

```
uv run pytest --pyargs cc26_tests                 # run the shipped suite, zero files in your repo
uv run pytest --pyargs cc26_tests -k "if/ and not fun/"   # subset by id
CT_PROVIDERS=corpus,fuzz_arith uv run pytest --pyargs cc26_tests
CT_PROVIDERS=corpus,cc26,tuples RUNTIME="..." uv run pytest --pyargs cc26_tests   # + optional lab 7
CT_PROVIDERS=corpus,tuples LINK="./build.sh {asm} {exe}" uv run pytest --pyargs cc26_tests
```

or pull the cases into your own tests (e.g. per-pass interpreter checks):

```python
from cc26_tests import cases  # list[pytest.param], ids = "provider/group/name"


@pytest.mark.parametrize("case", cases())
def test_my_pass(case): ...
```

Spiked: `--pyargs` on an installed package collects its tests, ships `cases/` as
package data and honours the package `conftest.py`. Config is env vars, so no
pytest plugin / custom CLI options are needed.

## Layout

```
pyproject.toml            deps: pytest (xdist optional); build backend uv_build or hatchling (ship every file, incl. .in/.out — not setuptools)
src/cc26_tests/
  __init__.py             Case, cases()
  providers.py            PROVIDERS registry + files/corpus/cc26 providers
  fuzz_<name>.py          one module per generator (later)
  run.py                  oracle (CPython) + compile/link/run, each with a timeout
  conftest.py             collect_ignore_glob = ["cases/*"]
  test_e2e.py             compile + gcc + run every selected case
  test_corpus.py          no compiler needed: oracle runs; agrees with .out where one exists
  cases/<group>/NAME.py [.in] [.out]   groups: var, if, loops, fun (cc26 chapters); tuples (opt-in)
```

## Case and providers

```python
@dataclass(frozen=True)
class Case:
    id: str  # "provider/group/name", stable across runs
    source: str
    stdin: str = ""
    expected: str | None = None  # None -> CPython oracle, computed lazily in the test
```

A provider is any `() -> Iterable[Case]`. No base class.

```python
PROVIDERS = {
    "corpus": corpus,
    "cc26": cc26,
    "tuples": tuples,
}  # + "fuzz_arith": fuzz_arith.cases when one exists
DEFAULT = ["corpus", "cc26"]  # fuzzers and optional labs opt-in
```

`CT_PROVIDERS` is a comma list of names. A generator living elsewhere can skip the
registry: `cases()` is just data, parametrize over your own list in your own test.

- `corpus`: `cases/` in this package, minus the opt-in groups.
- `tuples`: `cases/tuples/`, the optional lab 7 (ids `corpus/tuples/name`). Opt-in, so a
  compiler without tuples sees no new failures; `test_corpus.py` still checks these cases.
- `cc26`: `$CC26/tests/<chapter>_tests/*.py` minus `runtime.py`, `run_tests.py`; id
  `cc26/<group>/name`, group = folder minus `_tests`, same names as the corpus so `-k` spans both. Referenced
  by path, never copied (EOC licence).
- `fuzz_*`: seeded (`CT_SEED`, default 0), ids `fuzz/<gen>/<seed>-<i>`.

## Design rules (why)

- **Oracle runs inside the test, with a timeout (10 s)**, in a CPython subprocess
  (like cc26). A ~5-line `python -c` wrapper puts `input_int` into `builtins` *and*
  `sys.modules["runtime"]`, then `exec`s the source: covers bare `input_int()` (corpus)
  and `from runtime import input_int` (cc26). An oracle crash (e.g. cc26
  `loops_tests/06_call_in_loop` reads input but has no `.in`) fails that one test with the traceback. Collection only reads files, so a bad case or an infinite loop
  fails one test instead of hanging collection on every xdist worker.
- **Deterministic collection.** xdist workers each collect; ids and order must match.
  Providers sort, fuzzers seed.
- **Overflow:** the oracle wraps printed values to signed 64-bit. Exact only when the overflowing value goes straight to `print`; so don't compare or branch on a value past 2^63 (the oracle would disagree). `.out` is an optional pin that must agree with the oracle.
- **Subsets by id**, not marks: `-k "if/"`, `-k "not fun/"`.

## Updating

Git-sourced installs see new cases only after `uv lock --upgrade-package cc26-tests`.

## CI

One workflow, no compiler involved:

```
uv run ruff format --check
uv run ruff check        # cases: pyflakes only, builtins = ["input_int"]
uv run pytest src/cc26_tests/test_corpus.py
```

`ruff` is pinned in the dev group so everyone formats the same way. This is safe because
compilers read `ast.parse` output, which keeps no formatting (not even redundant parens).

## Not now

Pytest plugin with CLI options, marks per chapter, test minimiser, CI matrix over
everyone's compilers. Add when env vars / `-k` stop being enough.
