from dataclasses import dataclass, field 
from typing import List 
 
from ..analysis_objects.ir_route import Route 
from ..analysis_objects.ir_function import IRFunction 
from ..analysis_objects.ir_class import IRClass 
from ..analysis_objects.ir_event import IREvent 
from ..analysis_objects.ir_js_function import IRJSFunction 
 
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