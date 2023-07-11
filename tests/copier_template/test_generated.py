"""Test copier_template template."""

import logging
import os
import shutil
from logging import getLogger
from pathlib import Path

import black
import pytest
from copier import run_copy
from flake8.api import legacy as flake8
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
    style_guide_easy = flake8.get_style_guide(
        ignore=["E302", "E303", "E305", "F401", "W391"]
    )
    style_guide_strict = flake8.get_style_guide(
        ignore=[
            "F401",  # "imported but unused"
            "W292",  # "no newline at end of file"
            "W391",  # "blank line at end of file"
        ]
    )

    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "copier_template/"
    )

    run_copy(
        src_path=template_path,
        dst_path=outdir,
        data={
            "admin_name": "John Doe",
            "cli_prefix": "testflow",
            "extension_description": "A meltano utility extension for testflow that wraps the /bin/notreal command.",
            "extension_id": "testflow-ext",
            "extension_name": "Testflow",
            "extension_name_lower": "testflow",
            "library_name": "testflow_ext",
            "wrapper_target_name": "/bin/notreal",
        },
        quiet=True,
    )

    for outfile in Path(outdir).glob("**/*.py"):
        filepath = str(outfile.absolute())
        report = style_guide_easy.check_files([filepath])
        errors = report.get_statistics("E")
        assert (
            not errors
        ), f"Flake8 found violations in first pass of {filepath}: {errors}"
        mypy_out = api.run([filepath, "--config", str(Path(outdir) / Path("tox.ini"))])
        mypy_msg = str(mypy_out[0])
        if not mypy_msg.startswith("Success:"):
            logging.exception(f"MyPy validation failed: {mypy_msg}")
            assert not mypy_msg, f"MyPy validation failed for file {filepath}"
        report = style_guide_strict.check_files([filepath])
        errors = report.get_statistics("E")
        assert (
            not errors
        ), f"Flake8 found violations in second pass of {filepath}: {errors}"
        black.format_file_in_place(
            Path(filepath),
            fast=False,
            mode=black.FileMode(),
            write_back=black.WriteBack.NO,
        )
