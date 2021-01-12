import inspect
from .apply import passthrough


def assign(lhs, rhs, apply=passthrough):
    @on_change(rhs, apply=passthrough)
    def _():
        lhs.v = rhs.v


def on_change(*signals, apply=passthrough):
    def deco(func):
        @apply
        def callback(change):
            func()
        for s in signals:
            s.inst.observe(callback, s.name)
    return deco


def on_change_to(sig_val_dict=None, apply=passthrough, **sig_val):
    if sig_val_dict is None:
        caller_locals = inspect.currentframe().f_back.f_locals
        signals = [caller_locals[k] for k in sig_val.keys()]
        values = sig_val.values()
    else:
        signals = sig_val_dict.keys()
        values = sig_val_dict.values()
    def deco(func):
        @on_change(*signals, apply=apply)
        def _():
            for s, v in zip(signals, values):
                if s.v != v:
                    break
            else:
                func()
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
