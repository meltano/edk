import asyncio

import pytest
from mock import AsyncMock, Mock, patch

from meltano.edk.process import Invoker


@pytest.fixture()
def process_mock_factory():
    def _factory(name):
        process_mock = Mock()
        process_mock.name = name
        process_mock.wait = AsyncMock(return_value=0)
        process_mock.returncode = 0
        process_mock.stdin.wait_closed = AsyncMock(return_value=True)
        return process_mock

    return _factory


@pytest.fixture()
def process_mock(process_mock_factory):
    process = process_mock_factory("echo")
    process.stdout.at_eof.side_effect = (False, False, False, True)
    process.stdout.readline = AsyncMock(
        side_effect=(b"SCHEMA\n", b"RECORD\n", b"STATE\n")
    )
    process.stderr.at_eof.side_effect = (False, False, False, True)
    process.stderr.readline = AsyncMock(
        side_effect=(b"Starting\n", b"Running\n", b"Done\n")
    )
    process.sleep = AsyncMock()
    return process


def test_exec(process_mock):
    """Verify that the Invoker._exec method works as expected."""

    async def _test_exec():
        inv = Invoker("echo", cwd="/tmp", env={"FOO": "BAR"})
        with patch("asyncio.create_subprocess_exec") as mock:
            mock.return_value = process_mock
            await inv._exec("sub_command", "arg1", "arg2")
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
