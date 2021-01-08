import asyncio
from time import time
from threading import Timer


class AsyncTimer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()

    def start(self):
        self._task = asyncio.ensure_future(self._job())

    def cancel(self):
        self._task.cancel()


def debounce(wait, is_async=False):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            def call_it():
                fn(*args, **kwargs)
            if timer is not None:
                timer.cancel()
            if is_async:
                timer = AsyncTimer(wait, call_it)
            else:
                timer = Timer(wait, call_it)
            timer.start()
        return debounced
    return decorator


def throttle(wait, is_async=False):
    """ Decorator that prevents a function from being called
        more than once every wait period. """
    def decorator(fn):
        time_of_last_call = 0
        scheduled = False
        timer = None
        new_args, new_kwargs = None, None
        def throttled(*args, **kwargs):
            nonlocal new_args, new_kwargs, time_of_last_call, scheduled, timer
            def call_it():
                nonlocal new_args, new_kwargs, time_of_last_call, scheduled, timer
                time_of_last_call = time()
                fn(*new_args, **new_kwargs)
                scheduled = False
            new_args, new_kwargs = args, kwargs
            if not scheduled:
                scheduled = True
                time_since_last_call = time() - time_of_last_call
                new_wait = max(0, wait - time_since_last_call)
                if is_async:
                    timer = AsyncTimer(new_wait, call_it)
                else:
                    timer = Timer(new_wait, call_it)
                timer.start()
        return throttled
    return decorator
