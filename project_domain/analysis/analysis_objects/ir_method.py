# core/ir_system/typed_ir/ir_method.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IRMethod:
    name: str
    args: List[str]
    returns: Optional[str]
    calls: List[str]
    line: int
    symbol_id: str

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return IRMethod(**d)
