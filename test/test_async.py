import asyncio
from textwrap import dedent
from attrait import Signal, change


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
