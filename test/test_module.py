from textwrap import dedent
from attrait import Signal, on_change


def test_instance():
    s1 = Signal(init=0)
    s2 = Signal(init=0)
    s3 = Signal(init=0)

    def divider(inp, out):
        @on_change(inp)
        def _():
            if (inp.v % 2) == 0:
                out.v += 1

    divider(s1, s2)
    divider(s2, s3)

    res = ''
    for _ in range(9):
        res += f'{s1.v} {s2.v} {s3.v}\n'
        s1.v += 1

    ref = dedent('''\
        0 0 0
        1 0 0
        2 1 0
        3 1 0
        4 2 1
        5 2 1
        6 3 1
        7 3 1
        8 4 2
        ''')

    assert res == ref
