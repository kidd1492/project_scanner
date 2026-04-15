# core/ir_system/typed_ir.py
from dataclasses import dataclass, field
from typing import List, Optional


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


@dataclass
class IRFile:
    path: str
    source: str
    type: str
    routes: List[Route] = field(default_factory=list)
    # We’ll add functions/classes/imports/html_events/js_functions later
    # as we need them.


@dataclass
class ProjectIR:
    project_name: str
    total_files: int
    root: str
    file_types: list
    files: List[IRFile] = field(default_factory=list)
