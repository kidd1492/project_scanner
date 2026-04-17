# trace/trace_resolver.py
import re

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def normalize_js_api_call(api_call: str) -> str:
    if not api_call:
        return ""

    # Extract fetch("/path") or fetch('/path')
    m = re.search(r"fetch\s*\(\s*['\"]([^'\"]+)['\"]", api_call)
    if not m:
        return ""

    path = m.group(1)
    path = path.split("?", 1)[0]

    if not path.startswith("/"):
        path = "/" + path

    if path.endswith("/") and len(path) > 1:
        path = path[:-1]

    return path


def route_to_regex(route: str) -> str:
    # Convert Flask-style <id> to regex
    pattern = re.sub(r"<[^>]+>", r"[^/]+", route)
    return "^" + pattern + "$"


# ---------------------------------------------------------
# Typed IR Lookups
# ---------------------------------------------------------

def find_js_function(project_ir, trigger_name):
    func_name = trigger_name.split("(")[0]

    for f in project_ir.files:
        for fn in f.js_functions:
            if fn.name == func_name:
                return fn, f
    return None, None


def find_api_route_by_name(project_ir, route_name):
    for f in project_ir.files:
        for r in f.routes:
            if r.name == route_name:
                return r, f
    return None, None


def find_api_route_by_path(project_ir, js_api_call_line):
    js_path = normalize_js_api_call(js_api_call_line)
    if not js_path:
        return None, None

    for f in project_ir.files:
        for r in f.routes:
            if not r.route:
                continue

            route_regex = route_to_regex(r.route)
            if re.match(route_regex, js_path):
                return r, f

    return None, None


def find_python_function(project_ir, call_name):
    short = call_name.split(".")[-1]

    # Functions
    for f in project_ir.files:
        for fn in f.functions:
            if fn.name == short:
                return fn, f

    # Methods
    for f in project_ir.files:
        for cls in f.classes:
            for m in cls.methods:
                if m.name == short:
                    return m, f

    return None, None


# ---------------------------------------------------------
# Python Call Expansion
# ---------------------------------------------------------

def expand_python_calls(project_ir, call_list, visited=None):
    if visited is None:
        visited = set()

    children = []

    for call in call_list or []:
        resolved, file_obj = find_python_function(project_ir, call)
        if resolved is None:
            continue

        key = resolved.name

        if key in visited:
            children.append({
                "id": key,
                "type": "python",
                "meta": {"recursive": True, "file": file_obj.path},
                "children": [],
            })
            continue

        visited.add(key)

        sub_calls = resolved.calls
        node_children = expand_python_calls(project_ir, sub_calls, visited)

        children.append({
            "id": key,
            "type": "python",
            "meta": {
                "name": resolved.name,
                "file": file_obj.path,
            },
            "children": node_children,
        })

    return children


# ---------------------------------------------------------
# Root Resolver
# ---------------------------------------------------------

def resolve(project_ir, trigger_name):
    # JS entry
    js_entry, js_file = find_js_function(project_ir, trigger_name)
    if js_entry:
        return resolve_js(project_ir, js_entry, js_file)

    # API entry
    api_entry, api_file = find_api_route_by_name(project_ir, trigger_name)
    if api_entry:
        return resolve_api(project_ir, api_entry, api_file)

    # Python entry
    py_entry, py_file = find_python_function(project_ir, trigger_name)
    if py_entry:
        return resolve_python_root(project_ir, py_entry, py_file)

    return {
        "id": trigger_name,
        "type": "unknown",
        "meta": {"error": "Unknown trigger"},
        "children": [],
    }


# ---------------------------------------------------------
# JS Resolver
# ---------------------------------------------------------

def resolve_js(project_ir, js_entry, js_file):
    js_node = {
        "id": js_entry.name,
        "type": "js",
        "meta": {
            "name": js_entry.name,
            "file": js_file.path,
        },
        "children": [],
    }

    api_children = []

    api_calls = js_entry.api_call or []
    if isinstance(api_calls, str):
        api_calls = [api_calls]

    for api_call_line in api_calls:
        api_entry, api_file = find_api_route_by_path(project_ir, api_call_line)
        if api_entry:
            api_children.append(resolve_api(project_ir, api_entry, api_file))

    js_node["children"] = api_children
    return js_node


# ---------------------------------------------------------
# API Resolver
# ---------------------------------------------------------

def resolve_api(project_ir, api_entry, api_file):
    api_node = {
        "id": api_entry.name,
        "type": "api",
        "meta": {
            "name": api_entry.name,
            "route": api_entry.route,
            "file": api_file.path,
        },
        "children": [],
    }

    py_children = expand_python_calls(project_ir, api_entry.calls)
    api_node["children"] = py_children
    return api_node


# ---------------------------------------------------------
# Python Resolver
# ---------------------------------------------------------

def resolve_python_root(project_ir, py_entry, py_file):
    key = py_entry.name

    children = expand_python_calls(
        project_ir,
        py_entry.calls,
        visited={key},
    )

    return {
        "id": key,
        "type": "python",
        "meta": {
            "name": py_entry.name,
            "file": py_file.path,
        },
        "children": children,
    }
