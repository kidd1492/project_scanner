# core/analyzers/class_extractor.py
import ast

class ClassExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/")
        self.source = self.file_path.split("/")[-1]
        self.classes = []

    def visit_ClassDef(self, node):
        class_entry = {
            "type": "class",
            "name": node.name,
            "file": self.file_path,
            "source": self.source,
            "line": node.lineno,
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
                    "type": "method",
                    "name": item.name,
                    "args": [arg.arg for arg in item.args.args],
                    "calls": method_calls,
                    "returns": get_return_value(item),
                    "line": item.lineno
                })

        self.classes.append(class_entry)
        self.generic_visit(node)


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


class ImportExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/")
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                "type": "import",
                "module": alias.name,
                "symbol": None,
                "alias": alias.asname,
                "file": self.file_path,
                "source": self.file_path.split("/")[-1],
                "line": node.lineno
            })

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imports.append({
                "type": "import",
                "module": module,
                "symbol": alias.name,
                "alias": alias.asname,
                "file": self.file_path,
                "source": self.file_path.split("/")[-1],
                "line": node.lineno
            })


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


def get_call_name(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = get_call_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"
        return node.attr

    return None


def get_return_value(node):
    for child in ast.walk(node):
        if isinstance(child, ast.Return):
            try:
                return ast.unparse(child.value)
            except Exception:
                return None
    return None


def attach_parents(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
