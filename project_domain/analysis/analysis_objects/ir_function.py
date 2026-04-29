from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IRFunction:
    name: str
    args: List[str]
    returns: Optional[str]
    calls: List[str]
    file: str
    source: str
    line: int
    symbol_id: str

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return IRFunction(**d)
