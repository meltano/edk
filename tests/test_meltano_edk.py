from __future__ import annotations

from meltano.edk import models
from meltano.edk.extension import ExtensionBase


class TestExtension(ExtensionBase):
    def invoke(self, command_name: str | None, *command_args) -> None:
        pass

    def describe(self) -> models.Describe:
        return models.Describe(
            commands=[models.ExtensionCommand(name="test", description="test")]
        )


def test_canary():
    test = TestExtension()
    assert test.describe() == models.Describe(
        commands=[models.ExtensionCommand(name="test", description="test")]
    )
