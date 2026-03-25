import ast
from .helpers import get_call_name, get_return_value


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
    """Extract return expression as string."""
    for child in ast.walk(node):
        if isinstance(child, ast.Return):
            try:
                return ast.unparse(child.value)
            except Exception:
                return None
    return None


class RouteExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
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

        # Extract calls inside the function
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                name = get_call_name(child.func)
                if name:
                    calls.append(name)

        # Extract return value
        return_value = get_return_value(node)

        self.routes.append({
            "route": route_path,
            "function": node.name,
            "args": [arg.arg for arg in node.args.args],
            "returns": return_value,
            "calls": calls,
            "file": self.file_path
        })

        self.generic_visit(node)
