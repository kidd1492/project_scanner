# core/analyzers/route_extractor.py

import ast
from .helpers import get_call_name, get_return_value

class RouteExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/")
        self.source = self.file_path.split("/")[-1]
        self.routes = []

    def visit_FunctionDef(self, node):
        route_path = None

        # Detect @bp.route("/path")
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                func = decorator.func
                if isinstance(func, ast.Attribute) and func.attr == "route":
                    if decorator.args and isinstance(decorator.args[0], ast.Constant):
                        route_path = decorator.args[0].value

        if not route_path:
            return

        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                name = get_call_name(child.func)
                if name:
                    calls.append(name)

        self.routes.append({
            "type": "route",
            "name": node.name,
            "route": route_path,
            "args": [arg.arg for arg in node.args.args],
            "calls": calls,
            "returns": get_return_value(node),
            "file": self.file_path,
            "source": self.source,
            "line": node.lineno
        })

        self.generic_visit(node)
