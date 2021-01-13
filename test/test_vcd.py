import time
import os
import tempfile
from textwrap import dedent
from attrait import Signal
from vcd import VCDWriter
from vcd.gtkw import GTKWSave


def test_vcd():
    fdump = tempfile.NamedTemporaryFile(mode='wt', suffix='.vcd', delete=False)
    try:
        vcd_writer = VCDWriter(fdump, timescale='100 ms', date='today')
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.gtkw') as fsave:
            gtkw = GTKWSave(fsave)
            gtkw.dumpfile(fdump.name)
            s = Signal(vcd_writer=vcd_writer, gtkw=gtkw)

        vcd_writer.flush()

        for i in range(3):
            s.v = i
            time.sleep(0.1)
        for i in range(3, 0, -1):
            s.v = i
            time.sleep(0.1)

        vcd_writer.close()

    finally:
        fdump.close()
        with open(fdump.name) as f:
            res = f.read()
        os.remove(fdump.name)

    ref = dedent('''\
        $date today $end
        $timescale 100 ms $end
        $scope module  $end
        $var real 64 ! trait $end
        $upscope $end
        $enddefinitions $end
        #0
        $dumpvars
        r0 !
        $end
        #1
        r1 !
        #2
        r2 !
        #3
        r3 !
        #4
        r2 !
        #5
        r1 !
        ''')

    assert ref == res
