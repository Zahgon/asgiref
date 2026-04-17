import inspect

from .sync import iscoroutinefunction


def is_double_callable(application):
    """
    Tests to see if an application is a legacy-style (double-callable) application.
    """
    pass


def double_to_single_callable(application):
    """
    Transforms a double-callable ASGI application into a single-callable one.
    """
    pass


def guarantee_single_callable(application):
    """
    Takes either a single- or double-callable application and always returns it
    in single-callable style. Use this to add backwards compatibility for ASGI
    2.0 applications to your server/test harness/etc.
    """
    pass
