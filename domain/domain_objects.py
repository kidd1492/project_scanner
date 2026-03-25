# domain_objects.py
from typing import List, Optional
from dataclasses import dataclass, field


# -----------------------------
# FUNCTION
# -----------------------------
@dataclass
class Function:
    name: str
    parameters: List[str]
    returns: List[str]
    calls: List[str]
    parent_class: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "parameters": self.parameters,
            "returns": self.returns,
            "calls": self.calls,
            "parent_class": self.parent_class
        }


# -----------------------------
# CLASS
# -----------------------------
@dataclass
class Class:
    name: str
    methods: List[Function] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    inherits_from: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "methods": [m.to_dict() for m in self.methods],
            "attributes": self.attributes,
            "inherits_from": self.inherits_from
        }


# -----------------------------
# FILE
# -----------------------------
@dataclass
class File:
    path: str
    content: str
    functions: List[Function] = field(default_factory=list)
    classes: List[Class] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "path": self.path,
            "content": self.content,
            "imports": self.imports,
            "functions": [f.to_dict() for f in self.functions],
            "classes": [c.to_dict() for c in self.classes]
        }


# -----------------------------
# PROJECT SUMMARY
# -----------------------------
@dataclass
class ProjectSummary:
    name: str
    root: str
    total_files: int
    file_types: List[dict]   # {"type": "py", "count": 16, "files": [...]}
    has_readme: bool
    has_database: bool
    has_requirements: bool
    has_dockerfile: bool

    def to_dict(self):
        return {
            "name": self.name,
            "root": self.root,
            "total_files": self.total_files,
            "file_types": self.file_types,
            "has_readme": self.has_readme,
            "has_database": self.has_database,
            "has_requirements": self.has_requirements,
            "has_dockerfile": self.has_dockerfile
        }

@dataclass
class Trigger:
    event: str
    function: str
    file: str

    def to_dict(self):
        return {
            "event": self.event,
            "function": self.function,
            "file": self.file
        }

@dataclass
class Route:
    path: str
    method: str
    function_name: str
    file: str

    def to_dict(self):
        return {
            "path": self.path,
            "method": self.method,
            "function_name": self.function_name,
            "file": self.file
        }

@dataclass
class CallChain:
    trigger: Trigger
    js_function: Optional[str]
    api_route: Optional[Route]
    python_chain: List[Function]

    def to_dict(self):
        return {
            "trigger": self.trigger.to_dict(),
            "js_function": self.js_function,
            "api_route": self.api_route.to_dict() if self.api_route else None,
            "python_chain": [f.to_dict() for f in self.python_chain]
        }
