import asyncio
from traitlets import HasTraits, Int
from attrait import Signal, change


class Time(HasTraits):
    hour = Int()


async def clock(s):
    while True:
        await asyncio.sleep(1)
        s.v = s.v + 1


async def voice(s):
    while True:
        print('Time is:', s.v)
        await change(s)


async def alarm(s, t):
    while s.v < t:
        await change(s)
    print('Time to wake up!')


async def main():
    time = Time()
    s = Signal(time, 'hour')
    asyncio.create_task(clock(s))
    asyncio.create_task(voice(s))
    await alarm(s, 5)


asyncio.run(main())
