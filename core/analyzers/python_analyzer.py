# core/analyzers/python_analyzer.py

import ast
from .python_extractors import (
    RouteExtractor,
    ClassExtractor,
    FunctionExtractor,
    ImportExtractor,
    attach_parents,
)
from .base_analyzer import BaseAnalyzer
from core.ir_system.typed_ir import (
    Route,
    IRClass,
    IRMethod,
    IRFunction,
    IRFile,
)


class PythonAnalyzer(BaseAnalyzer):
    file_type = "py"

    def analyze_file(self, file: str) -> IRFile:
        file = file.replace("\\", "/")
        with open(file, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        attach_parents(tree)

        imp_ex = ImportExtractor(file)
        imp_ex.visit(tree)

        route_ex = RouteExtractor(file)
        route_ex.visit(tree)

        class_ex = ClassExtractor(file)
        class_ex.visit(tree)

        func_ex = FunctionExtractor(file)
        func_ex.visit(tree)

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
                symbol_id=f'{r["source"]}::{r["name"]}',
            )
            for r in route_ex.routes
        ]

        classes = []
        for c in class_ex.classes:
            methods = [
                IRMethod(
                    name=m["name"],
                    args=m.get("args", []),
                    returns=m.get("returns"),
                    calls=m.get("calls", []),
                    line=m["line"],
                    symbol_id=f'{c["source"]}::{c["name"]}.{m["name"]}',
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
                    symbol_id=f'{c["source"]}::{c["name"]}',
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
                symbol_id=f'{f_["source"]}::{f_["name"]}',
            )
            for f_ in func_ex.functions
        ]

        imports = [imp["module"] for imp in imp_ex.imports]

        return IRFile(
            path=file,
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

    def analyze_files(self, file_list):
        return [self.analyze_file(f) for f in file_list]
