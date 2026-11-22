"""Subprocess helpers: the CPython oracle and compile -> gcc -> run."""

import os
import shlex
import subprocess
import sys
from pathlib import Path

from cc26_tests.providers import CC26

RUNTIME_C = CC26 / "support" / "runtime.c"
# What gcc links the assembly with: $RUNTIME (shlex-split files and flags),
# default cc26's runtime.c. Tuples need one with initialize and collect.
RUNTIME = shlex.split(os.environ["RUNTIME"]) if "RUNTIME" in os.environ else None
DEFAULT_COMPILER = "uv run compiler.py {src} -o {out}"

# input_int both bare (corpus) and via `from runtime import input_int` (cc26);
# whitespace-separated like runtime.c's scanf("%ld"). print wraps to signed 64-bit.
ORACLE = """
import builtins, sys, types

tokens = iter(sys.stdin.read().split())

def input_int():
    return int(next(tokens))

def print_int(x):
    x = int(x) & (1 << 64) - 1
    sys.stdout.write(f"{x - (1 << 64) if x >= 1 << 63 else x}\\n")

builtins.input_int, builtins.print = input_int, print_int
sys.modules["runtime"] = types.SimpleNamespace(input_int=input_int)
exec(sys.argv[1], {"__name__": "__main__"})
"""


def run(cmd: list[str | Path], what: str, timeout: float, stdin: str = "") -> str:
    """stdout of cmd; a non-zero exit fails the test with the output tail."""
    r = subprocess.run(
        cmd, input=stdin, capture_output=True, text=True, timeout=timeout
    )
    if r.returncode != 0:
        tail = "\n".join((r.stderr or r.stdout).strip().splitlines()[-10:])
        raise AssertionError(f"{what} exited with {r.returncode}:\n{tail}")
    return r.stdout


def oracle(source: str, stdin: str) -> str:
    """What the program should print, according to CPython."""
    return run([sys.executable, "-I", "-c", ORACLE, source], "oracle", 10, stdin)


def compile_and_run(source: str, stdin: str, tmp: Path) -> str:
    """$COMPILER with {src}/{out} filled in, then gcc, then the binary."""
    src, asm, exe = tmp / "prog.py", tmp / "prog.s", tmp / "prog"
    src.write_text(source)
    template = os.environ.get("COMPILER", DEFAULT_COMPILER)
    cmd = [
        a.replace("{src}", str(src)).replace("{out}", str(asm))
        for a in shlex.split(template)
    ]
    run(cmd, "compiler", 30)
    runtime = RUNTIME if RUNTIME is not None else [RUNTIME_C]
    run(["gcc", "-o", exe, asm, *runtime, "-Wl,-z,noexecstack"], "gcc", 30)
    return run([exe], "program", 10, stdin)
