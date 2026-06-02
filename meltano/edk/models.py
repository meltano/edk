"""Various models used to describe extensions."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Command:
    """Describe a generic runnable command."""

    name: str
    description: str
    commands: list[str] = field(default_factory=list)
    pass_through_cli: bool = False


@dataclass(slots=True)
class ExtensionCommand(Command):
    """Describes an extension command."""

    description: str = "The extension cli"
    pass_through_cli: bool = False
    commands: list[str] = field(
        default_factory=lambda: [
            "describe",
            "invoke",
            "pre_invoke",
            "post_invoke",
            "initialize",
        ]
    )


@dataclass(slots=True)
class InvokerCommand(Command):
    """Describes an invoker style command."""

    description: str = "The pass through invoker cli"
    pass_through_cli: bool = True
    commands: list[str] = field(default_factory=lambda: [":splat"])


@dataclass(slots=True)
class Describe:
    """Describes what commands and capabilities the extension provides."""

    commands: list[Command]
