# core/analyzers/python_analyzer.py

import ast
from pathlib import Path

from .base_analyzer import BaseAnalyzer
from .python_extractors import (
    RouteExtractor,
    ClassExtractor,
    FunctionExtractor,
    ImportExtractor,
    attach_parents,
)
from project_domain.project_ir_builer_service.analysis_objects import (
    Route,
    IRClass,
    IRMethod,
    IRFunction,
)
from project_domain.project_ir_builer_service.analysis_objects.ir_file import IRFile

class PythonAnalyzer(BaseAnalyzer):
    file_type = "py"

    """TODO move this to the infrastructure/file_system/file_repository.py
    discover_files and list_files"""
    def analyze_file(self, path: str, content: str) -> IRFile:
        # Normalize path
        file = path.replace("\\", "/")
        path = Path(file)
        source_code = content

        tree = ast.parse(source_code)
        attach_parents(tree)

        # Run extractors
        imp_ex = ImportExtractor(file)
        imp_ex.visit(tree)

        route_ex = RouteExtractor(file)
        route_ex.visit(tree)

        class_ex = ClassExtractor(file)
        class_ex.visit(tree)

        func_ex = FunctionExtractor(file)
        func_ex.visit(tree)

        # Build IR objects
        routes = [
            Route(
                name=r["name"],
                route=r["route"],
                args=r.get("args", []),
                calls=r.get("calls", []),
                returns=r.get("returns"),
                file=r["file"],
                source=r["source"],
                line=r["line"],
                symbol_id=f'{r["source"]} :: {r["name"]}',
            )
            for r in route_ex.routes
        ]

        classes: list[IRClass] = []
        for c in class_ex.classes:
            methods = [
                IRMethod(
                    name=m["name"],
                    args=m.get("args", []),
                    returns=m.get("returns"),
                    calls=m.get("calls", []),
                    line=m["line"],
                    symbol_id=f'{c["source"]} :: {c["name"]}.{m["name"]}',
                )
                for m in c.get("methods", [])
            ]

            classes.append(
                IRClass(
                    name=c["name"],
                    methods=methods,
                    file=c["file"],
                    source=c["source"],
                    line=c["line"],
                    symbol_id=f'{c["source"]} :: {c["name"]}',
                )
            )

        functions = [
            IRFunction(
                name=f_["name"],
                args=f_.get("args", []),
                returns=f_.get("returns"),
                calls=f_.get("calls", []),
                file=f_["file"],
                source=f_["source"],
                line=f_["line"],
                symbol_id=f'{f_["source"]} :: {f_["name"]}',
            )
            for f_ in func_ex.functions
        ]

        imports = [imp["module"] for imp in imp_ex.imports]

        return IRFile(
            path=str(path),
            source=source_code,
            type="py",
            routes=routes,
            functions=functions,
            classes=classes,
            imports=imports,
            html_events=[],
            js_functions=[],
            api_calls=[],
        )
