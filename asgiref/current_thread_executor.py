import sys
import threading
from collections import deque
from concurrent.futures import Executor, Future
from typing import Any, Callable, TypeVar

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

_T = TypeVar("_T")
_P = ParamSpec("_P")
_R = TypeVar("_R")


class _WorkItem:
    """
    Represents an item needing to be run in the executor.
    Copied from ThreadPoolExecutor (but it's private, so we're not going to rely on importing it)
    """

    def __init__(
        self,
        future: "Future[_R]",
        fn: Callable[_P, _R],
        *args: _P.args,
        **kwargs: _P.kwargs,
    ):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        pass


class CurrentThreadExecutor(Executor):
    """
    An Executor that actually runs code in the thread it is instantiated in.
    Passed to other threads running async code, so they can run sync code in
    the thread they came from.
    """

    def __init__(self, old_executor: "CurrentThreadExecutor | None") -> None:
        self._work_thread = threading.current_thread()
        self._work_ready = threading.Condition(threading.Lock())
        self._work_items = deque[_WorkItem]()  # synchronized by _work_ready
        self._broken = False  # synchronized by _work_ready
        self._old_executor = old_executor

    def run_until_future(self, future: "Future[Any]") -> None:
        """
        Runs the code in the work queue until a result is available from the future.
        Should be run from the thread the executor is initialised in.
        """
        pass

    def submit(
        self,
        fn: Callable[_P, _R],
        /,
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> "Future[_R]":
        # Check they're not submitting from the same thread
        pass
