# This code is originally sourced from the aio-libs project "async_timeout",
# under the Apache 2.0 license. You may see the original project at
# https://github.com/aio-libs/async-timeout

# It is vendored here to reduce chain-dependencies on this library, and
# modified slightly to remove some features we don't use.


import asyncio
import warnings
from types import TracebackType
from typing import Any  # noqa
from typing import Optional, Type


class timeout:
    """timeout context manager.

    Useful in cases when you want to apply timeout logic around block
    of code or in cases when asyncio.wait_for is not suitable. For example:

    >>> with timeout(0.001):
    ...     async with aiohttp.get('https://github.com') as r:
    ...         await r.text()


    timeout - value in seconds or None to disable timeout logic
    loop - asyncio compatible event loop
    """

    def __init__(
        self,
        timeout: Optional[float],
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._timeout = timeout
        if loop is None:
            loop = asyncio.get_running_loop()
        else:
            warnings.warn(
                """The loop argument to timeout() is deprecated.""", DeprecationWarning
            )
        self._loop = loop
        self._task = None  # type: Optional[asyncio.Task[Any]]
        self._cancelled = False
        self._cancel_handler = None  # type: Optional[asyncio.Handle]
        self._cancel_at = None  # type: Optional[float]

    def __enter__(self) -> "timeout":
        return self._do_enter()

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> Optional[bool]:
        self._do_exit(exc_type)
        return None

    async def __aenter__(self) -> "timeout":
        return self._do_enter()

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        self._do_exit(exc_type)

    @property
    def expired(self) -> bool:
        pass

    @property
    def remaining(self) -> Optional[float]:
        pass

    def _do_enter(self) -> "timeout":
        # Support Tornado 5- without timeout
        # Details: https://github.com/python/asyncio/issues/392
        pass

    def _do_exit(self, exc_type: Type[BaseException]) -> None:
        pass

    def _cancel_task(self) -> None:
        pass
