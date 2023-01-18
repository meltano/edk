from __future__ import annotations

import structlog

from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.types import ExecArg


class CustomExtension(ExtensionBase):
    def __init__(self) -> None:
        super().__init__()
        self.history: list[tuple[str | None, tuple[ExecArg, ...]]] = []

    def pre_invoke(self, invoke_name: str | None, *command_args: ExecArg) -> None:
        self.history.append((invoke_name, ("pre", *command_args)))

    def invoke(self, command_name: str | None, *command_args: ExecArg) -> None:
        self.history.append((command_name, command_args))

    def post_invoke(self, invoked_name: str | None, *command_args: ExecArg) -> None:
        self.history.append((invoked_name, ("post", *command_args)))

    def describe(self) -> models.Describe:
        return models.Describe(
            commands=[models.ExtensionCommand(name="test", description="test")]
        )


def test_canary():
    test = CustomExtension()
    assert test.describe() == models.Describe(
        commands=[models.ExtensionCommand(name="test", description="test")]
    )


def test_invoke():
    test = CustomExtension()
    test.invoke("echo", "test")
    assert test.history == [("echo", ("test",))]


def test_pass_through():
    test = CustomExtension()
    logger = structlog.getLogger("test")
    test.pass_through_invoker(logger, "test")
    assert test.history == [
        (None, ("pre", "test")),
        (None, ("test",)),
        (None, ("post", "test")),
    ]
