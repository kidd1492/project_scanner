import ast
from .helpers import get_call_name, get_return_value


class ClassExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/")
        self.classes = []

    def visit_ClassDef(self, node):
        class_entry = {
            "class": node.name,
            "file": self.file_path,
            "methods": []
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_calls = []
                for child in ast.walk(item):
                    if isinstance(child, ast.Call):
                        name = get_call_name(child.func)
                        if name:
                            method_calls.append(name)

                class_entry["methods"].append({
                    "method": item.name,
                    "args": [arg.arg for arg in item.args.args],
                    "calls": method_calls,
                    "returns": get_return_value(item)
                })

        self.classes.append(class_entry)
        self.generic_visit(node)
