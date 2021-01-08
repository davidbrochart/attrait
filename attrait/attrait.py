import asyncio
import inspect

from traitlets import HasTraits, Any
from .apply import debounce, throttle


class Traiteur(HasTraits):
    trait = Any()


class Signal:

    def __init__(self,
                 inst : HasTraits = None,
                 name : str = None):

        if inst is None:
            self.inst = Traiteur()
            self.name = 'trait'
        else:
            self.inst = inst
            self.name = name

    @property
    def v(self):
        return getattr(self.inst, self.name)

    @v.setter
    def v(self, value):
        setattr(self.inst, self.name,  value)


def passthrough(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


async def any_change(*signals, apply=passthrough):
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


def on_any_change(decorator=passthrough):
    def deco(func):
        caller_locals = inspect.currentframe().f_back.f_locals
        signals = [caller_locals[name] for name in inspect.signature(func).parameters]
        @decorator
        def callback(change):
            func(*signals)
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
