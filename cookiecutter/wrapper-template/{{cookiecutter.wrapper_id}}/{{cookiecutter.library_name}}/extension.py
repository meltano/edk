"""Meltano {{ cookiecutter.extension_name }} extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import structlog

from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

log = structlog.get_logger()


class {{ cookiecutter.extension_name }}(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.{{ cookiecutter.extension_name_lower }}_bin = "{{ cookiecutter.wrapper_target_name }}"  # verify this is the correct name
        self.{{ cookiecutter.extension_name_lower }}_invoker = Invoker(self.{{ cookiecutter.extension_name_lower }}_bin)

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.{{ cookiecutter.extension_name_lower }}_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                f"{{ cookiecutter.extension_name_lower }} {command_name}", err, "{{ cookiecutter.extension_name }} invocation failed"
            )
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        # TODO: could we auto-generate all or portions of this from typer instead?
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="{{ cookiecutter.cli_prefix }}_extension", description="extension commands"
                ),
                models.InvokerCommand(
                    name="{{ cookiecutter.cli_prefix }}_invoker", description="pass through invoker"
                ),
            ]
        )
