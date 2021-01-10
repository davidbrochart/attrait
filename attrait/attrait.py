import asyncio
import inspect

from .signal import Signal
from .apply import debounce, throttle


def passthrough(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


async def change(*signals, apply=passthrough):
    event = asyncio.Event()
    @apply
    def callback(value):
        event.set()
    for s in signals:
        s.inst.observe(callback, s.name)
    await event.wait()
    for s in signals:
        s.inst.unobserve(callback, s.name)


async def all_change(*signals, apply=passthrough):
    '''All the signals must change values, meaning that changing to a value then
    changing back to the original value is not considered a change.
    '''
    event = asyncio.Event()
    @apply
    def callback(value):
        event.set()
    for s in signals:
        s.inst.observe(callback, s.name)
    old_values = [s.v for s in signals]
    while True:
        await event.wait()
        event.clear()
        if all([v != s.v for v, s in zip(old_values, signals)]):
            break
    for s in signals:
        s.inst.unobserve(callback, s.name)


def on_change(*signals, apply=passthrough):
    def deco(func):
        @apply
        def callback(change):
            func()
        for s in signals:
            s.inst.observe(callback, s.name)
    return deco


def on_all_change(decorator=passthrough):
    '''All the signals must change values, meaning that changing to a value then
    changing back to the original value is not considered a change.
    '''
    def deco(func):
        caller_locals = inspect.currentframe().f_back.f_locals
        signals = [caller_locals[name] for name in inspect.signature(func).parameters]
        old_values = [s.v for s in signals]
        def wrapper(*signals):
            if all([v != s.v for v, s in zip(old_values, signals)]):
                old_values = [s.v for s in signals]
                func(*signals)
        @decorator
        def callback(change):
            wrapper(*signals)
        for s in signals:
            s.inst.observe(callback, s.name)
    return deco
