import asyncio
import inspect


class Signal:
    def __init__(self, inst, name):
        self.inst = inst
        self.name = name

    @property
    def v(self):
        return getattr(self.inst, self.name)

    @v.setter
    def v(self, value):
        setattr(self.inst, self.name,  value)


async def any_change(*args):
    event = asyncio.Event()
    def callback(value):
        event.set()
    for s in args:
        s.inst.observe(callback, s.name)
    await event.wait()
    for s in args:
        s.inst.unobserve(callback, s.name)


async def all_change(*args):
    event = asyncio.Event()
    def callback(value):
        event.set()
    for s in args:
        s.inst.observe(callback, s.name)
    change_nb = 0;
    while change_nb < len(args):
        await event.wait()
        event.clear()
        change_nb += 1
    for s in args:
        s.inst.unobserve(callback, s.name)


def on_any_change(func):
    caller_locals = inspect.currentframe().f_back.f_locals
    inputs = [caller_locals[name] for name in inspect.signature(func).parameters]
    def callback(change):
        func(*inputs)
    for s in inputs:
        s.inst.observe(callback, s.name)


def on_all_change(func):
    caller_locals = inspect.currentframe().f_back.f_locals
    inputs = [caller_locals[name] for name in inspect.signature(func).parameters]
    old_values = [s.v for s in inputs]
    def wrapper(*inputs):
        diff = True
        for i, s in enumerate(inputs):
            if old_values[i] == s.v:
                diff = False
                break
            old_values[i] = s.v
        if diff:
            func(*inputs)
    def callback(change):
        wrapper(*inputs)
    for s in inputs:
        s.inst.observe(callback, s.name)
