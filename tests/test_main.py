"""Run from the `pyta` root directory to use the local `python_ta` rather than
installed `python_ta` package.
"""

import subprocess
import sys
from os import environ

import python_ta


def test_check_no_errors_zero() -> None:
    """Test that python_ta exits with status code 0 when it does not detect errors."""
    output = subprocess.run(
        [
            sys.executable,
            "-m",
            "python_ta",
            "--config",
            "tests/test.pylintrc",
            "tests/fixtures/no_errors.py",
        ]
    )

    assert output.returncode == 0


def test_check_errors_nonzero() -> None:
    """Test that python_ta exits with non-zero status code when it detects errors."""
    output = subprocess.run(
        [
            sys.executable,
            "-m",
            "python_ta",
            "--config",
            "tests/test.pylintrc",
            "examples/nodes/name.py",
        ]
    )

    assert output.returncode != 0


def test_check_exit_zero() -> None:
    """Test that python_ta --exit-zero always exits with status code 0,
    even when given a file with errors.
    """
    output = subprocess.run(
        [
            sys.executable,
            "-m",
            "python_ta",
            "--exit-zero",
            "--config",
            "tests/test.pylintrc",
            "examples/nodes/name.py",
        ],
        env={**environ, "PYTHONIOENCODING": "utf-8"},
    )

    assert output.returncode == 0


def test_check_version() -> None:
    """Test that python_ta --version outputs python_ta.__version__ to stdout."""
    stdout = subprocess.run(
        [
            sys.executable,
            "-m",
            "python_ta",
            "--config",
            "tests/test.pylintrc",
            "--version",
        ],
        capture_output=True,
        text=True,
    ).stdout

    assert stdout.rstrip("\n") == python_ta.__version__


def test_config_generation() -> None:
    """Test that python_ta --generate-config prints the default config to stdout."""
    stdout_config = subprocess.run(
        [
            sys.executable,
            "-m",
            "python_ta",
            "--generate-config",
            "--config",
            "tests/test.pylintrc",
        ],
        capture_output=True,
        text=True,
    ).stdout.rstrip("\n")

    actual_config = subprocess.run(
        [
            "cat",
            "python_ta/config/.pylintrc",
        ],
        capture_output=True,
        text=True,
    ).stdout.rstrip("\n")

    assert stdout_config == actual_config


def test_no_config() -> None:
    """Test that python_ta exits with status code 0 when it does not detect errors
    and no config is specified.

    NOTE: The exit code 0 for this file is already tested; this merely confirms that
          the absence of a config does not affect the process.
    """
    output = subprocess.run(
        [
            sys.executable,
            "-m",
            "python_ta",
            "--output-format",
            "python_ta.reporters.PlainReporter",
            "tests/fixtures/no_errors.py",
        ],
    )

    assert output.returncode == 0