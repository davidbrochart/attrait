import asyncio
from traitlets import HasTraits, Int
from attrait import Signal, any_change, all_change


class Time(HasTraits):
    hour = Int()
    minute = Int()


async def clock(h, m):
    while True:
        await asyncio.sleep(1)
        m.v = m.v + 30
        await asyncio.sleep(1)
        m.v = 0
        h.v = h.v + 1


async def voice(h,m ):
    while True:
        print('Time is:', f'{h.v}h{m.v}')
        await any_change(h, m)


async def alarm(h, m, t):
    while h.v < t:
        await any_change(h)
    print('Time to wake up!')
    await all_change(h, m)
    print('You have snoozed!')


async def main():
    time = Time()
    h = Signal(time, 'hour')
    m = Signal(time, 'minute')
    asyncio.create_task(clock(h, m))
    asyncio.create_task(voice(h, m))
    await alarm(h, m, 3)


asyncio.run(main())
