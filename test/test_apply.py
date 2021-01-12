import time
import asyncio
from attrait import Signal, on_change, debounce, throttle


def test_debounce_sync():
    s = Signal(init=0)

    counter = Signal(init=0)

    @on_change(s, apply=debounce(0.1))
    def _():
        counter.v += 1

    s.v += 1
    # wait long enough, the next change is not filtered out
    time.sleep(0.11)
    s.v += 1
    # don't wait long enough, the next change is filtered out
    time.sleep(0.9)
    s.v += 1

    assert counter.v == 2



def test_throttle_sync():
    s = Signal(init=0)

    counter = Signal(init=0)

    @on_change(s, apply=throttle(0.13))
    def _():
        counter.v += 1

    for _ in range(5):
        s.v += 1
        time.sleep(0.1)

    assert counter.v == 4



def test_debounce_async():
    async def main():
        s = Signal(init=0)

        counter = Signal(init=0)

        @on_change(s, apply=debounce(0.1))
        def _():
            counter.v += 1

        s.v += 1
        # wait long enough, the next change is not filtered out
        await asyncio.sleep(0.11)
        s.v += 1
        # don't wait long enough, the next change is filtered out
        await asyncio.sleep(0.9)
        s.v += 1

        assert counter.v == 2

    asyncio.run(main())



def test_throttle_async():
    async def main():
        s = Signal(init=0)

        counter = Signal(init=0)

        @on_change(s, apply=throttle(0.13))
        def _():
            counter.v += 1

        for _ in range(5):
            s.v += 1
            await asyncio.sleep(0.1)
            s.v += 1

        assert counter.v == 4

    asyncio.run(main())
