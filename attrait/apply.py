import asyncio
from time import time
from threading import Timer


def passthrough(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class AsyncTimer:
    def __init__(self, timeout, callback, args, kwargs):
        self._timeout = timeout
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback(*self._args, **self._kwargs)

    def start(self):
        self._task = asyncio.ensure_future(self._job())

    def cancel(self):
        self._task.cancel()


def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    class Decorator:
        def __init__(self):
            self.is_async = False
            self.timer = None
        def debounced(self, *args, **kwargs):
            if self.timer is not None:
                self.timer.cancel()
            if self.is_async:
                self.timer = AsyncTimer(wait, self.fn, args, kwargs)
            else:
                self.timer = Timer(wait, self.fn, args, kwargs)
            self.timer.start()
        def __call__(self, fn):
            self.fn = fn
            return self.debounced
    return Decorator()


def throttle(wait):
    """ Decorator that prevents a function from being called
        more than once every `wait` period. """
    class Decorator:
        def __init__(self):
            self.is_async = False
            self.time_of_last_call = 0
            self.scheduled = False
        def call_it(self, *args, **kwargs):
            self.time_of_last_call = time()
            self.fn(*args, **kwargs)
            self.scheduled = False
        def throttled(self, *args, **kwargs):
            if not self.scheduled:
                self.scheduled = True
                time_since_last_call = time() - self.time_of_last_call
                new_wait = max(0, wait - time_since_last_call)
                if self.is_async:
                    self.timer = AsyncTimer(new_wait, self.call_it, args, kwargs)
                else:
                    self.timer = Timer(new_wait, self.call_it, args, kwargs)
                self.timer.start()
        def __call__(self, fn):
            self.fn = fn
            return self.throttled
    return Decorator()


def delay(wait):
    """ Decorator that will delay by `wait` seconds. """
    class Decorator:
        def __init__(self):
            self.is_async = False
        def delayed(self, *args, **kwargs):
            if self.is_async:
                self.timer = AsyncTimer(wait, self.fn, args, kwargs)
            else:
                self.timer = Timer(wait, self.fn, args, kwargs)
            self.timer.start()
        def __call__(self, fn):
            self.fn = fn
            return self.delayed
    return Decorator()
