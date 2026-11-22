"""A provider is any () -> Iterable[Case]. Sorted, deterministic, cheap."""

import os
from collections.abc import Iterable
from pathlib import Path

from cc26_tests import Case

CASES_DIR = Path(__file__).parent / "cases"
# The course repo, relative to where pytest runs (a student repo has it as a submodule).
CC26 = Path(os.environ.get("CC26", "cc26"))
CC26_NOT_CASES = {"runtime.py", "run_tests.py"}  # as in cc26's run_tests.py


def read_case(path: Path, id: str) -> Case:
    """NAME.py with optional NAME.in and NAME.out beside it."""
    stdin, out = path.with_suffix(".in"), path.with_suffix(".out")
    return Case(
        id=id,
        source=path.read_text(),
        stdin=stdin.read_text() if stdin.exists() else "",
        expected=out.read_text() if out.exists() else None,
    )


# Groups for optional labs: in the package, but only run when asked for.
OPT_IN_GROUPS = {"tuples"}


def corpus_group(group: str) -> list[Case]:
    return [
        read_case(p, f"corpus/{group}/{p.stem}")
        for p in sorted((CASES_DIR / group).glob("*.py"))
    ]


def corpus() -> Iterable[Case]:
    """cases/<group>/NAME.py in this package, opt-in groups excepted."""
    groups = sorted(d.name for d in CASES_DIR.iterdir() if d.is_dir())
    return [c for g in groups if g not in OPT_IN_GROUPS for c in corpus_group(g)]


def tuples() -> Iterable[Case]:
    """cases/tuples: the optional lab 7. Needs a runtime with a heap, see RUNTIME."""
    return corpus_group("tuples")


def cc26() -> Iterable[Case]:
    """$CC26/tests/<group>_tests/*.py; empty when CC26 is not checked out."""
    return [
        read_case(p, f"cc26/{p.parent.name.removesuffix('_tests')}/{p.stem}")
        for p in sorted((CC26 / "tests").glob("*_tests/*.py"))
        if p.name not in CC26_NOT_CASES
    ]


PROVIDERS = {"corpus": corpus, "cc26": cc26, "tuples": tuples}
DEFAULT = ["corpus", "cc26"]  # fuzzers and optional labs are opt-in
