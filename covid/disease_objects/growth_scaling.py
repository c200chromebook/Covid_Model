from datetime import datetime
from functools import reduce
from operator import mul
from covid.util.util import parse_tuple_list


class GrowthScaling:
    def __init__(self, cfg):
        self.multipliers = {}
        for multiplier_row in cfg['GROWTH_SCALING']:
            self.multipliers[multiplier_row] = {datetime.strptime(date, "%Y-%m-%d"): float(mult)
                                                for date, mult
                                                in parse_tuple_list(cfg['GROWTH_SCALING'][multiplier_row])}

    def __getitem__(self,date):
        def floor_lookup(needle, haystack):
            if needle < min(list(haystack.keys())):
                return 1.0
            return haystack[max(k for k in haystack.keys() if k <= needle)]
        return reduce(mul, [floor_lookup(date, self.multipliers[multiplier]) for multiplier in self.multipliers], 1.0)

