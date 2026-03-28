import ast, json, os


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


def analyze_project(directory: str):
    allowed_extensions = [
        ".py", ".html", ".js", ".md", ".txt", ".db",
        ".css", ".rst", ".yml"
    ]
    ignored_directories = [".git", "env", "venv", "__pycache__"]

    categorized = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                ext = file.split('.')[-1]
                full_path = os.path.abspath(os.path.join(root, file))
                categorized.setdefault(ext, []).append(full_path)

    file_types = [
        {"type": ext, "count": len(paths), "files": paths}
        for ext, paths in categorized.items()
    ]

    data = {
        "project_name": os.path.basename(directory),
        "root": directory,
        "file_types": file_types
    }

    return data


def save_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return