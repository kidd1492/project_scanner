# core/ir_system/typed_ir.py
from dataclasses import dataclass, field
from typing import List, Optional


# -----------------------------
# Route
# -----------------------------
@dataclass
class Route:
    name: str
    route: str
    args: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    returns: Optional[str] = None
    file: str = ""
    source: str = ""
    line: int = 0
    symbol_id: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "route": self.route,
            "args": self.args,
            "calls": self.calls,
            "returns": self.returns,
            "file": self.file,
            "source": self.source,
            "line": self.line,
            "symbol_id": self.symbol_id,
            "type": "route",
        }


# -----------------------------
# IRFunction
# -----------------------------
@dataclass
class IRFunction:
    name: str
    args: List[str] = field(default_factory=list)
    returns: Optional[str] = None
    calls: List[str] = field(default_factory=list)
    file: str = ""
    source: str = ""
    line: int = 0
    symbol_id: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "args": self.args,
            "returns": self.returns,
            "calls": self.calls,
            "file": self.file,
            "source": self.source,
            "line": self.line,
            "symbol_id": self.symbol_id,
            "type": "function",
        }


# -----------------------------
# IRMethod
# -----------------------------
@dataclass
class IRMethod:
    name: str
    args: List[str] = field(default_factory=list)
    returns: Optional[str] = None
    calls: List[str] = field(default_factory=list)
    line: int = 0
    symbol_id: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "args": self.args,
            "returns": self.returns,
            "calls": self.calls,
            "line": self.line,
            "symbol_id": self.symbol_id,
            "type": "method",
        }


# -----------------------------
# IRClass
# -----------------------------
@dataclass
class IRClass:
    name: str
    methods: List["IRMethod"] = field(default_factory=list)
    file: str = ""
    source: str = ""
    line: int = 0
    symbol_id: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "methods": [m.to_dict() for m in self.methods],
            "file": self.file,
            "source": self.source,
            "line": self.line,
            "symbol_id": self.symbol_id,
            "type": "class",
        }


# -----------------------------
# IREvent
# -----------------------------
@dataclass
class IREvent:
    name: str
    handler: str = ""
    file: str = ""
    source: str = ""
    line: int = 0
    symbol_id: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "handler": self.handler,
            "file": self.file,
            "source": self.source,
            "line": self.line,
            "symbol_id": self.symbol_id,
            "type": "event",
        }


# -----------------------------
# IRJSFunction
# -----------------------------
@dataclass
class IRJSFunction:
    name: str
    args: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    file: str = ""
    source: str = ""
    line: int = 0
    symbol_id: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "args": self.args,
            "calls": self.calls,
            "file": self.file,
            "source": self.source,
            "line": self.line,
            "symbol_id": self.symbol_id,
            "type": "js_function",
        }


# -----------------------------
# IRFile
# -----------------------------
@dataclass
class IRFile:
    path: str
    source: str
    type: str

    routes: List[Route] = field(default_factory=list)
    functions: List["IRFunction"] = field(default_factory=list)
    classes: List["IRClass"] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    html_events: List["IREvent"] = field(default_factory=list)
    js_functions: List["IRJSFunction"] = field(default_factory=list)
    api_calls: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "source": self.source,
            "type": self.type,
            "routes": [r.to_dict() for r in self.routes],
            "functions": [fn.to_dict() for fn in self.functions],
            "classes": [cls.to_dict() for cls in self.classes],
            "imports": self.imports,
            "html_events": [ev.to_dict() for ev in self.html_events],
            "js_functions": [js.to_dict() for js in self.js_functions],
            "api_calls": self.api_calls,
        }


# -----------------------------
# ProjectIR
# -----------------------------
@dataclass
class ProjectIR:
    project_name: str
    total_files: int
    root: str
    file_types: list
    files: List[IRFile] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "total_files": self.total_files,
            "root": self.root,
            "file_types": self.file_types,
            "files": [f.to_dict() for f in self.files],
        }

    def find_file(self, path: str) -> Optional[IRFile]:
        for f in self.files:
            if f.path == path:
                return f
        return None

    def find_symbol(self, symbol_id: str):
        # Routes
        for f in self.files:
            for r in f.routes:
                if r.symbol_id == symbol_id:
                    return r

        # Functions
        for f in self.files:
            for fn in f.functions:
                if fn.symbol_id == symbol_id:
                    return fn

        # Classes
        for f in self.files:
            for cls in f.classes:
                if cls.symbol_id == symbol_id:
                    return cls
                for m in cls.methods:
                    if m.symbol_id == symbol_id:
                        return m

        # HTML events
        for f in self.files:
            for ev in f.html_events:
                if ev.symbol_id == symbol_id:
                    return ev

        # JS functions
        for f in self.files:
            for js in f.js_functions:
                if js.symbol_id == symbol_id:
                    return js

        return None
