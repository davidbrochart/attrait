from time import time
from typing import Optional
from traitlets import HasTraits, Any
from vcd import VCDWriter
from vcd.gtkw import GTKWSave, GTKWFlag


def make_trait(name='trait', ttype=None, init=None):
    if ttype is None:
        ttype = Any
    if init is None:
        type_inst = ttype()
    else:
        type_inst = ttype(init)
    Traiteur = type('Traiteur', (HasTraits, ), {name: type_inst})
    return Traiteur()


class Signal:

    def __init__(self,
                 inst : Optional[HasTraits] = None,
                 name : Optional[str] = None,
                 type = None,
                 init = None,
                 vcd_writer : Optional[VCDWriter] = None,
                 gtkw : Optional[GTKWSave] = None):

        name = name or 'trait'
        self.name = name
        if inst is None:
            self.inst = make_trait(name=name, ttype=type, init=init)
        else:
            if type is not None:
                 raise RuntimeError('Cannot set the type of an already existing trait.')
            self.inst = inst
            if init is not None:
                setattr(inst, name, init)
        self.vcd_writer = vcd_writer
        if vcd_writer is not None:
            self.vcd_var = vcd_writer.register_var('', name, 'real', init=0)
            self.time0 = time()
            if gtkw is not None:
                gtkw.trace(
                    name,
                    datafmt='real',
                    extraflags=GTKWFlag.analog_step | GTKWFlag.analog_fullscale,
                )
                gtkw.blank(analog_extend=True)
                gtkw.blank(analog_extend=True)
                gtkw.blank(analog_extend=True)

    @property
    def v(self):
        return getattr(self.inst, self.name)

    @v.setter
    def v(self, value):
        setattr(self.inst, self.name,  value)
        if self.vcd_writer is not None:
            self.vcd_writer.change(self.vcd_var, 10 * (time() - self.time0), value)
            self.vcd_writer.flush()
