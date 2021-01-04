import asyncio


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


async def change(s):
    event = asyncio.Event()
    def callback(value):
        event.set()
    s.inst.observe(callback, s.name)
    await event.wait()
    s.inst.unobserve(callback, s.name)
