"""Test copier_template template."""

import os
import shutil
import subprocess
from logging import getLogger

import pytest
from copier import run_copy
from mypy import api

getLogger("flake8").propagate = False


@pytest.fixture(scope="class")
def outdir() -> str:
    """Create a temporary directory for cookiecutters."""
    name = ".output/"
    try:
        os.mkdir(name)
    except FileExistsError:
        shutil.rmtree(name)
        os.mkdir(name)

    yield name
    shutil.rmtree(name)


def test_copier_output(outdir: str):
    """Generate and validate the resulting copier managed template."""
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "copier_template/"
    )

    run_copy(
        src_path=template_path,
        dst_path=outdir,
        data={
            "admin_name": "John Doe",
            "cli_prefix": "testflow",
            "extension_description": "A meltano utility extension for testflow that wraps the /bin/notreal command.",  # noqa: E501
            "extension_id": "testflow-ext",
            "extension_name": "Testflow",
            "extension_name_lower": "testflow",
            "library_name": "testflow_ext",
            "wrapper_target_name": "/bin/notreal",
        },
        quiet=True,
    )

    # Use mypy to check the generated code
    mypy_stdout, mypy_stderr, mypy_exit_status = api.run([outdir])
    assert not mypy_exit_status, mypy_stdout

    # Use ruff to check the generated code
    ruff_check = [
        "ruff",
        "check",
        outdir,
        "--select",
        "E,F,W,Q",
    ]
    p = subprocess.run(ruff_check, capture_output=True)
    assert p.returncode == 0, p.stdout.decode("utf-8")

    # Use ruff to format the generated code
    ruff_format = [
        "ruff",
        "format",
        outdir,
        "--check",
    ]
    p = subprocess.run(ruff_format, capture_output=True)
    assert p.returncode == 0, p.stdout.decode("utf-8")
