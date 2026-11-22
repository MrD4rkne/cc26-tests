# cc26-tests

Shared end-to-end tests for our cc26 compilers. Assumption: **several people,
several compilers**, one shared corpus. The harness treats a compiler as a
black box: source in, x86 assembly out.

## Quick start

Add it as a dev dependency of your compiler repo:

```toml
[dependency-groups]
dev = ["cc26-tests"]

[tool.uv.sources]
cc26-tests = { git = "https://github.com/MrD4rkne/cc26-tests" }
```

Then, from your repo root (the course repo checked out as `./cc26`):

```sh
uv run pytest --pyargs cc26_tests
```

Each test compiles one program, links it, runs it, and compares what it prints
with what CPython prints. Nothing else to set up if your compiler runs as
`uv run compiler.py prog.py -o prog.s`.

## Settings

All settings are environment variables. Commands are split like a shell would
(`shlex.split`) and run from pytest's working directory.

| Variable | Default | What it does |
|---|---|---|
| `COMPILER` | `uv run compiler.py {src} -o {out}` | Compiles `{src}` (a `.py`) to `{out}` (a `.s`). |
| `RUNTIME` | `$CC26/support/runtime.c` | Files and flags gcc links with the assembly. |
| `LINK` | gcc, see below | Your own link command, with `{asm}` and `{exe}`. Wins over `RUNTIME`. |
| `CC26` | `./cc26` | The course repo: gives `runtime.c` and the `cc26` cases. |
| `CT_PROVIDERS` | `corpus,cc26` | Which cases to run, comma list (see [Providers](#case-and-providers)). |

Without `LINK`, the link step is
`gcc -o {exe} {asm} $RUNTIME -Wl,-z,noexecstack`.

Compiler prints the assembly to stdout instead? Use
`COMPILER="sh -c 'uv run compiler.py {src} > {out}'"`.

A test fails when the compiler, the link step or the program exits non-zero
(you get the last lines of its output), on a timeout (30 s compile, 30 s link,
10 s run), or when the program's output differs from CPython's. Outputs are
compared as whitespace-separated words, like cc26's `run_tests.py`.

If `$CC26/support/runtime.c` is missing and neither `RUNTIME` nor `LINK` is set,
the end-to-end tests are skipped with a reason, and the `cc26` provider has no cases.

## Examples

```sh
uv run pytest --pyargs cc26_tests -k "if/ and not fun/"    # a subset, by test id
uv run pytest --pyargs cc26_tests -n auto                  # in parallel (pytest-xdist)
CT_PROVIDERS=corpus uv run pytest --pyargs cc26_tests      # only our own cases
```

## Lab 7: tuples

The `tuples` cases are opt-in: they need a runtime with a heap and a collector,
so a compiler without tuples sees no new failures. Turn them on, and link
`runtime-full.c` in one of two ways.

**Your own link script** (simplest if you already have one):

```sh
CT_PROVIDERS=corpus,cc26,tuples LINK="./build.sh {asm} {exe}" \
  uv run pytest --pyargs cc26_tests
```

**Or a prebuilt object.** `runtime-full.c` has its own `print_int` and includes
your `runtime.h`, so compile it once with `print_int` renamed:

```sh
gcc -c -w -I<dir with your runtime.h> -Dprint_int=rt_print_int \
  cc26/support/runtime-full.c -o build/runtime-full.o
CT_PROVIDERS=corpus,cc26,tuples RUNTIME="build/runtime-full.o cc26/support/runtime.c" \
  uv run pytest --pyargs cc26_tests
```

**Use a small heap.** The garbage-collection cases allocate about 1.5 MB in
total. With a bigger heap the collector never runs, and a broken one still
passes. Pass a small heap to your compiler, e.g.
`COMPILER="uv run compiler.py --heap-size 64 {src} -o {out}"`.

## Use the cases in your own tests

`cases()` is plain data, e.g. for per-pass interpreter checks:

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
  providers.py            PROVIDERS registry + corpus/tuples/cc26 providers
  fuzz_<name>.py          one module per generator (later)
  run.py                  oracle (CPython) + compile/link/run, each with a timeout
  conftest.py             collect_ignore_glob = ["cases/*"]
  test_e2e.py             compile + link + run every selected case
  test_corpus.py          no compiler needed: oracle runs on every case; agrees with .out where one exists
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
- `tuples`: `cases/tuples/`, the optional lab 7 (ids `corpus/tuples/name`). Opt-in, see
  [Lab 7](#lab-7-tuples); `test_corpus.py` still checks these cases.
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
