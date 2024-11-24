from dataclasses import dataclass
from typing import Tuple

TUPLE_LEN = 3

@dataclass
class ReversibleColor:

    tuple_val: Tuple[float, float, float]
    inverse: Tuple[float, float, float]

    def __invert__(self):
        return ReversibleColor(self.inverse, self.tuple_val)

    def __iter__(self):
        for i in range(TUPLE_LEN):
            yield self.tuple_val[i]
