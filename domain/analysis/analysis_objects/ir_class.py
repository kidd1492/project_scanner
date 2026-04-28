from dataclasses import dataclass
from typing import List

from .ir_method import IRMethod

@dataclass
class IRClass:
    name: str
    methods: List[IRMethod]
    file: str
    source: str
    line: int
    symbol_id: str

    def get_methods(self):
        return self.methods

    def to_dict(self):
        return {
            "name": self.name,
            "methods": [m.to_dict() for m in self.methods],
            "file": self.file,
            "source": self.source,
            "line": self.line,
            "symbol_id": self.symbol_id,
        }

    @staticmethod
    def from_dict(d):
        return IRClass(
            name=d["name"],
            methods=[IRMethod.from_dict(m) for m in d["methods"]],
            file=d["file"],
            source=d["source"],
            line=d["line"],
            symbol_id=d["symbol_id"],
        )
