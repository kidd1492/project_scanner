# project_domain/dashboard_factory/dashboard_ir.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DashboardIR:
    project_name: str
    root: str
    total_files: int

    file_type_counts: Dict[str, int]
    symbol_counts: Dict[str, int]

    routes: int
    js_functions: int
    html_events: int
    api_calls: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "root": self.root,
            "total_files": self.total_files,
            "file_type_counts": self.file_type_counts,
            "symbol_counts": self.symbol_counts,
            "routes": self.routes,
            "js_functions": self.js_functions,
            "html_events": self.html_events,
            "api_calls": self.api_calls,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DashboardIR":
        return DashboardIR(
            project_name=d["project_name"],
            root=d["root"],
            total_files=d["total_files"],
            file_type_counts=d["file_type_counts"],
            symbol_counts=d["symbol_counts"],
            routes=d["routes"],
            js_functions=d["js_functions"],
            html_events=d["html_events"],
            api_calls=d["api_calls"],
        )
