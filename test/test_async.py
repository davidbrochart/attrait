import asyncio
from textwrap import dedent
from attrait import Signal, change, change_to


def test_change_to():
    s1 = Signal(init=0)
    s2 = Signal(init=0)

    async def main():
        assert s1.v == 0
        assert s2.v == 0
        await change_to(s1=2, s2=1)
        assert s1.v == 2
        assert s2.v == 1


def test_coroutine():
    s = Signal(init=0)

    async def writer():
        for i in range(3):
            await asyncio.sleep(0.01)
            s.v += 1

    async def reader():
        global res
        res = ''
        while True:
            await change(s)
            res += f'{s.v}\n'

    async def main():
        asyncio.create_task(reader())
        asyncio.create_task(writer())
        await asyncio.sleep(0.05)

    asyncio.run(main())

    ref = dedent('''\
        1
        2
        3
        ''')

    assert ref == res
