from attrait import Signal, on_change_to, assign


def test_on_change_to():
    s1 = Signal(init=0)
    s2 = Signal(init=0)
    s3 = Signal(init=0)

    @on_change_to(s1=2, s2=1)
    def _():
        s3.v = 1

    s1.v = 1
    assert s3.v == 0
    s2.v = 1
    assert s3.v == 0
    s1.v = 2
    assert s3.v == 1


def test_assign():
    s1 = Signal(init=0)
    s2 = Signal(init=0)

    assign(s1, s2)

    assert s1.v == 0
    assert s2.v == 0
    s2.v = 1
    assert s1.v == 1
