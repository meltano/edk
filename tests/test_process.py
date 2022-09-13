import asyncio
from unittest.mock import AsyncMock, patch

from meltano.edk.process import Invoker


def test_exec():
    """Verify that the Invoker._exec method works as expected."""

    async def _test_exec():
        inv = Invoker("echo", cwd="/tmp", env={"FOO": "BAR"})
        with patch("asyncio.create_subprocess_exec") as mock:
            mock.return_value = AsyncMock()
            await inv._exec("sub_command", ["arg1", "arg2"])
            mock.assert_called_once_with(
                "echo",
                "sub_command",
                "arg1",
                "arg2",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd="/tmp",
                env={"FOO": "BAR"},
            )

    asyncio.run(_test_exec())
