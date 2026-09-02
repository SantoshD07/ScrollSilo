import sys

import pytest

from scrollsilo.download import run


def test_run_returns_stdout():
    assert run([sys.executable, "-c", "print('hi')"]).strip() == "hi"


def test_run_failure_includes_stderr_message():
    cmd = [sys.executable, "-c", "import sys; sys.stderr.write('certificate boom'); sys.exit(3)"]
    with pytest.raises(RuntimeError, match="certificate boom"):
        run(cmd)