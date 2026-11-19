"""Guards our own cases; needs no compiler."""

import pytest

from cc26_tests import Case
from cc26_tests.providers import corpus
from cc26_tests.run import oracle


@pytest.mark.parametrize("case", corpus(), ids=lambda c: c.id)
def test_oracle_runs_and_agrees_with_out_file(case: Case) -> None:
    got = oracle(case.source, case.stdin)
    if case.expected is not None:
        assert got.split() == case.expected.split()
