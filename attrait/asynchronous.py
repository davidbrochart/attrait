import asyncio
import inspect
from .apply import passthrough


async def change_to(sig_val_dict=None, apply=passthrough, **sig_val):
    apply.is_async = True
    if sig_val_dict is None:
        caller_locals = inspect.currentframe().f_back.f_locals
        signals = [caller_locals[k] for k in sig_val.keys()]
        values = sig_val.values()
    else:
        signals = sig_val_dict.keys()
        values = sig_val_dict.values()
    while True:
        for s, v in zip(signals, values):
            if s.v != v:
                break
        else:
            break
        await change(*signals, apply=apply)


async def change(*signals, apply=passthrough):
    apply.is_async = True
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
