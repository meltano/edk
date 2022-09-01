"""Passthrough shim for {{ cookiecutter.source_name }} extension."""
import sys

import structlog

from {{ cookiecutter.library_name }}.wrapper import {{ cookiecutter.source_name }}
from meltano_extension_sdk.logging import pass_through_logging_config


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = {{cookiecutter.source_name}}()
    ext.pass_through_invoker(
        structlog.getLogger("{{ cookiecutter.cli_prefix }}_invoker"),
        *sys.argv[1:] if len(sys.argv) > 1 else []
    )
