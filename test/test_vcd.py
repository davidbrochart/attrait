import time
from attrait import Signal
from vcd import VCDWriter
from vcd.gtkw import GTKWSave, GTKWFlag, spawn_gtkwave_interactive


ref = '''\
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
'''

def test_vcd():
    fdump = open('dump.vcd', 'wt')
    vcd_writer = VCDWriter(fdump, timescale='100 ms', date='today')
    fsave = open('dump.gtkw', 'wt')
    gtkw = GTKWSave(fsave)
    gtkw.dumpfile('dump.vcd')

    s = Signal(vcd_writer=vcd_writer, gtkw=gtkw)
    fsave.close()
    vcd_writer.flush()

    for i in range(3):
        s.v = i
        time.sleep(0.1)
    for i in range(3, 0, -1):
        s.v = i
        time.sleep(0.1)

    vcd_writer.close()
    fdump.close()

    with open('dump.vcd') as f:
        res = f.read()

    assert ref == res
