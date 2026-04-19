# core/ir_system/typed_ir/ir_js_function.py

from dataclasses import dataclass
from typing import List

@dataclass
class IRJSFunction:
    name: str
    args: List[str]
    calls: List[str]
    api_call: str
    file: str
    source: str
    line: int
    symbol_id: str

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return IRJSFunction(**d)
