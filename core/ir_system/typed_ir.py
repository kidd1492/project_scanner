# core/ir_system/typed_ir.py

from dataclasses import dataclass, field
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


@dataclass
class IRMethod:
    name: str
    args: List[str]
    returns: Optional[str]
    calls: List[str]
    line: int
    symbol_id: str


@dataclass
class IRClass:
    name: str
    methods: List[IRMethod]
    file: str
    source: str
    line: int
    symbol_id: str


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


# -------------------------
# NEW: JS + HTML IR TYPES
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


@dataclass
class IREvent:
    event: str
    name: str
    file: str
    source: str
    line: int
    symbol_id: str


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
            "routes": [r.__dict__ for r in self.routes],
            "functions": [f.__dict__ for f in self.functions],
            "classes": [
                {
                    **c.__dict__,
                    "methods": [m.__dict__ for m in c.methods]
                }
                for c in self.classes
            ],
            "imports": self.imports,
            "html_events": [e.__dict__ for e in self.html_events],
            "js_functions": [j.__dict__ for j in self.js_functions],
            "api_calls": self.api_calls,
        }


@dataclass
class ProjectIR:
    project_name: str
    total_files: int
    root: str
    file_types: list
    files: List[IRFile]

    def to_dict(self):
        return {
            "project_name": self.project_name,
            "total_files": self.total_files,
            "root": self.root,
            "file_types": self.file_types,
            "files": [f.to_dict() for f in self.files],
        }
