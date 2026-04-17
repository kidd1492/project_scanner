from dataclasses import dataclass

@dataclass
class IREvent:
    event: str
    name: str
    file: str
    source: str
    line: int
    symbol_id: str

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return IREvent(**d)
