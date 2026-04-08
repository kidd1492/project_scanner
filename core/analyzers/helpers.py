import ast


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
