"""Guards our own cases and the harness; needs no compiler."""

from pathlib import Path

import pytest

from cc26_tests import Case
from cc26_tests.providers import CASES_DIR, corpus_group
from cc26_tests.run import link, oracle


# Every case in the package, opt-in groups included.
@pytest.mark.parametrize(
    "case",
    [
        c
        for d in sorted(CASES_DIR.iterdir())
        if d.is_dir()
        for c in corpus_group(d.name)
    ],
    ids=lambda c: c.id,
)
def test_oracle_runs_and_agrees_with_out_file(case: Case) -> None:
    got = oracle(case.source, case.stdin)
    if case.expected is not None:
        assert got.split() == case.expected.split()


def test_link_fills_the_template(tmp_path: Path) -> None:
    asm, exe = tmp_path / "prog.s", tmp_path / "prog"
    asm.write_text("assembly")
    link(asm, exe, "cp {asm} {exe}")
    assert exe.read_text() == "assembly"
