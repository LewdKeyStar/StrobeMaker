from dataclasses import dataclass

@dataclass
class Resolution:
    width: int
    height: int

    def to_tuple(self):
        return (self.width, self.height)
