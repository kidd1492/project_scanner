# core/ir_system/typed_ir.py

from dataclasses import dataclass, field
from typing import List, Optional


# -------------------------
# ROUTES
# -------------------------

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


# -------------------------
# METHODS
# -------------------------

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


# -------------------------
# CLASSES
# -------------------------

@dataclass
class IRClass:
    name: str
    methods: List[IRMethod]
    file: str
    source: str
    line: int
    symbol_id: str

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


# -------------------------
# PYTHON FUNCTIONS
# -------------------------

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


# -------------------------
# JS FUNCTIONS
# -------------------------

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


# -------------------------
# HTML EVENTS
# -------------------------

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


# -------------------------
# IR FILE
# -------------------------

@dataclass
class IRFile:
    path: str
    source: str
    type: str
    routes: List[Route] = field(default_factory=list)
    functions: List[IRFunction] = field(default_factory=list)
    classes: List[IRClass] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    html_events: List[IREvent] = field(default_factory=list)
    js_functions: List[IRJSFunction] = field(default_factory=list)
    api_calls: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "path": self.path,
            "source": self.source,
            "type": self.type,
            "routes": [r.to_dict() for r in self.routes],
            "functions": [f.to_dict() for f in self.functions],
            "classes": [c.to_dict() for c in self.classes],
            "imports": self.imports,
            "html_events": [e.to_dict() for e in self.html_events],
            "js_functions": [j.to_dict() for j in self.js_functions],
            "api_calls": self.api_calls,
        }

    @staticmethod
    def from_dict(d):
        return IRFile(
            path=d["path"],
            source=d["source"],
            type=d["type"],
            routes=[Route.from_dict(r) for r in d["routes"]],
            functions=[IRFunction.from_dict(f) for f in d["functions"]],
            classes=[IRClass.from_dict(c) for c in d["classes"]],
            imports=d["imports"],
            html_events=[IREvent.from_dict(e) for e in d["html_events"]],
            js_functions=[IRJSFunction.from_dict(j) for j in d["js_functions"]],
            api_calls=d["api_calls"],
        )


