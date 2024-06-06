"""Utilities for working with subprocesses."""

from __future__ import annotations

import asyncio
import os
import signal
import subprocess
import sys
import typing as t

import structlog

from meltano.edk.types import ExecArg

log = structlog.get_logger()


def log_subprocess_error(
    cmd: str, err: subprocess.CalledProcessError, error_message: str
) -> None:
    """Log a subprocess error, replaying stderr to the logger if it's available.

    Args:
        cmd: the command that was run.
        err: the error that was raised.
        error_message: the error message to log.
    """
    if err.stderr:
        for line in err.stderr.split("\n"):
            log.warning(line, cmd=cmd, stdio_stream="stderr")
    log.error(
        f"error invoking {cmd}",
        returncode=err.returncode,
        error_message=error_message,
    )


class Invoker:
    """Invoker utility class for invoking subprocesses."""

    def __init__(
        self,
        bin: str,
        cwd: str | None = None,
        env: dict[str, t.Any] | None = None,
    ) -> None:
        """Minimal invoker for running subprocesses.

        Args:
            bin: The path/name of the binary to run.
            cwd: The working directory to run from.
            env: Env to use when calling Popen, defaults to current os.environ if None.
        """
        self.bin = bin
        self.cwd = cwd
        self.popen_env = env if env else os.environ.copy()

    def run(
        self,
        *args: ExecArg,
        stdout: None | int | t.IO = subprocess.PIPE,
        stderr: None | int | t.IO = subprocess.PIPE,
        text: bool = True,
        **kwargs: t.Any,
    ) -> subprocess.CompletedProcess:
        """Run a subprocess. Simple wrapper around subprocess.run.

        Note that output from stdout and stderr is NOT logged automatically. Especially
        useful when you want to run a command, but don't care about its output and only
        care about its return code.

        stdout and stderr by default are set up to use subprocess.PIPE. If you do not
        want to capture io from the subprocess use subprocess.DEVNULL to discard it.

        The Invoker's at env and cwd are used when calling `subprocess.run`. If you want
        to override these you're likely better served using `subprocess.run` directly.

        Lastly note that this method is blocking AND `subprocess.run` is called with
        `check=True`. This means that if the subprocess fails a `CalledProcessError`
        will be raised.

        Args:
            *args: The arguments to pass to the subprocess.
            stdout: The stdout stream to use.
            stderr: The stderr stream to use.
            text: If true, decode stdin, stdout and stderr using the system default.
            **kwargs: Additional keyword arguments to pass to subprocess.run.

        Returns:
            The completed process.
        """
        return subprocess.run(
            [self.bin, *args],
            cwd=self.cwd,
            env=self.popen_env,
            stdout=stdout,
            stderr=stderr,
            check=True,
            text=text,
            **kwargs,
        )

    @staticmethod
    async def _log_stdio(reader: asyncio.streams.StreamReader) -> None:
        """Log the output of a stream.

        Args:
            reader: The stream reader to read from.
        """
        while True:
            if reader.at_eof():
                break
            data = await reader.readline()
            log.info(data.decode("utf-8").rstrip())
            await asyncio.sleep(0)

    async def _exec(
        self,
        sub_command: str | None = None,
        *args: ExecArg,
    ) -> asyncio.subprocess.Process:
        popen_args: list[ExecArg] = []
        if sub_command:
            popen_args.append(sub_command)
        if args:
            popen_args.extend(args)

        p = await asyncio.create_subprocess_exec(
            self.bin,
            *popen_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.cwd,
            env=self.popen_env,
        )

        loop = asyncio.get_event_loop()
        # Windows does not support add_signal_handler
        # https://docs.python.org/3/library/asyncio-platforms.html
        if sys.platform != "win32":
            loop.add_signal_handler(
                signal.SIGINT,
                lambda s=signal.SIGINT: p.send_signal(s),  # type: ignore[misc]
            )

        streams: list[asyncio.streams.StreamReader] = []

        if p.stderr:
            streams.append(p.stderr)

        if p.stdout:
            streams.append(p.stdout)

        results = await asyncio.gather(
            *[asyncio.create_task(self._log_stdio(stream)) for stream in streams],
            return_exceptions=True,
        )

        for r in results:  # raise first exception if any
            if isinstance(r, Exception):
                raise r

        await p.wait()
        return p

    def run_and_log(
        self,
        sub_command: str | None = None,
        *args: ExecArg,
    ) -> None:
        """Run a subprocess and stream the output to the logger.

        Note that output from stdout and stderr IS logged. Best used when you want
        to run a command and stream the output to a user.

        Args:
            sub_command: The subcommand to run.
            *args: The arguments to pass to the subprocess.

        Raises:
            CalledProcessError: If the subprocess failed.
        """
        result = asyncio.run(self._exec(sub_command, *args))
        if result.returncode:
            raise subprocess.CalledProcessError(
                result.returncode, cmd=self.bin, stderr=None
            )
