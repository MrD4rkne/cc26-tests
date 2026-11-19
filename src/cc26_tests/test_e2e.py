"""Every selected case through $COMPILER, gcc and the binary."""

import shutil
from pathlib import Path

import pytest

from cc26_tests import Case, cases
from cc26_tests.run import RUNTIME_C, compile_and_run, oracle


@pytest.mark.skipif(shutil.which("gcc") is None, reason="gcc not installed")
@pytest.mark.skipif(not RUNTIME_C.exists(), reason=f"{RUNTIME_C} missing, set CC26")
@pytest.mark.parametrize("case", cases())
def test_compiled_program_prints_expected_output(case: Case, tmp_path: Path) -> None:
    expected = case.expected
    if expected is None:
        expected = oracle(case.source, case.stdin)
    assert (
        compile_and_run(case.source, case.stdin, tmp_path).split() == expected.split()
    )
