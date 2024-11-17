from dataclasses import dataclass
from typing import ClassVar

class InvalidColorException(Exception):
    pass

@dataclass
class BWColor:

    valid_string_vars: ClassVar[list[str]] = ["BLACK", "WHITE"]

    int_val: int = 0

    def __init__(self, string_val: str):
        self.int_val = BWColor.str_to_int(string_val)

    def __invert__(self):
        return BWColor("BLACK" if self.int_val == 255 else "WHITE")

    def __int__(self):
        return self.int_val

    @classmethod
    def str_to_int(cls, string_val: str):
        if string_val not in BWColor.valid_string_vars:
            raise InvalidColorException("BWColor only accepts BLACK or WHITE values")

        return 255 if string_val == "WHITE" else 0
