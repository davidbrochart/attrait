from time import sleep
from traitlets import HasTraits, Int
from attrait import Signal, on_change


class Counter(HasTraits):
    i1 = Int()
    i2 = Int()


counter = Counter()
s_i1 = Signal(counter, 'i1')
s_i2 = Signal(counter, 'i2')


@on_change([s_i1])
def _(inputs):
    s_i1, = inputs
    print('i1 =', s_i1.v)
    if (s_i1.v % 2) == 0:
        s_i2.v += 1


@on_change([s_i2])
def _(inputs):
    s_i2, = inputs
    print('        i2 =', s_i2.v)


while True:
    s_i1.v = s_i1.v + 1
    sleep(1)
