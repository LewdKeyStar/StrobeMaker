from dataclasses import dataclass



@dataclass
class Resolution:
    width: int
    height: int

    def __iter__(self):
        val_list = list(self.__dict__.values())

        for value in val_list:
            yield value
