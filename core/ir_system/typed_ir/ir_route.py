from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Route:
    name: str
    route: str
    args: List[str]
    calls: List[str]
    returns: Optional[str]
    file: str
    source: str
    line: int
    symbol_id: str

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Route(**d)

