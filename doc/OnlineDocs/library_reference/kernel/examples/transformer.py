import pyomo.environ
import pyomo.kernel

import pympler.asizeof


def _fmt(num, suffix='B'):
    """format memory output"""
    if num is None:
        return "<unknown>"
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1000.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


# @kernel
class Transformer(pyomo.kernel.block):
    def __init__(self):
        super(Transformer, self).__init__()
        self._a = pyomo.kernel.parameter()
        self._v_in = pyomo.kernel.expression()
        self._v_out = pyomo.kernel.expression()
        self._c = pyomo.kernel.constraint(self._a * self._v_out == self._v_in)

    def set_ratio(self, a):
        assert a > 0
        self._a.value = a

    def connect_v_in(self, v_in):
        self._v_in.expr = v_in

    def connect_v_out(self, v_out):
        self._v_out.expr = v_out


# @kernel

print("Memory:", _fmt(pympler.asizeof.asizeof(Transformer())))


# @aml
def Transformer():
    b = pyomo.environ.Block(concrete=True)
    b._a = pyomo.environ.Param(mutable=True)
    b._v_in = pyomo.environ.Expression()
    b._v_out = pyomo.environ.Expression()
    b._c = pyomo.environ.Constraint(expr=b._a * b._v_out == b._v_in)
    return b


# @aml

print("Memory:", _fmt(pympler.asizeof.asizeof(Transformer())))
