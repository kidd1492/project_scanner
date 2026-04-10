# core/analyzers/function_extractor.py

import ast
from .helpers import get_call_name, get_return_value

class FunctionExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/")
        self.source = self.file_path.split("/")[-1]
        self.functions = []

    def visit_FunctionDef(self, node):
        # Skip class methods
        if isinstance(getattr(node, "parent", None), ast.ClassDef):
            return

        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                name = get_call_name(child.func)
                if name:
                    calls.append(name)

        self.functions.append({
            "type": "function",
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "calls": calls,
            "returns": get_return_value(node),
            "file": self.file_path,
            "source": self.source,
            "line": node.lineno
        })

        self.generic_visit(node)
