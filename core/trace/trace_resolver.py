import re
from core.ir_system.typed_ir import ProjectIR, IRFile, IRFunction, IRClass, IRMethod, IRJSFunction, IREvent, Route


def normalize_js_api_call(api_call):
    if not api_call:
        return ""

    m = re.search(r'fetch\s*\(\s*[\'"`]([^\'"`]+)[\'"`]', api_call)
    if not m:
        return ""

    path = m.group(1)
    path = path.split("?")[0]

    if not path.startswith("/"):
        path = "/" + path

    path = re.sub(r'^/(chat_route|ingestion|research|retrieval)', '', path)

    if path.endswith("/"):
        path = path[:-1]

    return path


def route_to_regex(route):
    pattern = re.sub(r"<[^>]+>", r"[^/]+", route)
    return "^" + pattern + "$"


# -----------------------------
# IR search helpers (typed IR)
# -----------------------------
def _find_js_function(project_ir: ProjectIR, trigger_name: str):
    func_name = trigger_name.split("(")[0]

    for f in project_ir.files:
        for fn in f.js_functions:
            if fn.name == func_name:
                meta = fn.to_dict()
                meta["file"] = f.path
                return meta
    return None


def _find_api_route_by_name(project_ir: ProjectIR, route_name: str):
    for f in project_ir.files:
        for r in f.routes:
            if r.name == route_name:
                meta = r.to_dict()
                meta["file"] = f.path
                return meta
    return None


def _find_api_route_by_path(project_ir: ProjectIR, js_api_call_line: str):
    js_path = normalize_js_api_call(js_api_call_line)
    if not js_path:
        return None

    for f in project_ir.files:
        for r in f.routes:
            route_pattern = r.route
            if not route_pattern:
                continue
            route_regex = route_to_regex(route_pattern)
            if re.match(route_regex, js_path):
                meta = r.to_dict()
                meta["file"] = f.path
                return meta
    return None


def _find_python_function(project_ir: ProjectIR, call_name: str):
    short = call_name.split(".")[-1]

    # Free functions
    for f in project_ir.files:
        for fn in f.functions:
            if fn.name == short:
                meta = fn.to_dict()
                meta["file"] = f.path
                meta["full_name"] = call_name
                meta["kind"] = "function"
                return meta

    # Class methods
    for f in project_ir.files:
        for cls in f.classes:
            cls_name = cls.name
            for m in cls.methods:
                if m.name == short:
                    meta = m.to_dict()
                    meta["file"] = f.path
                    meta["class"] = cls_name
                    meta["full_name"] = call_name
                    meta["kind"] = "method"
                    return meta

    return None


# -----------------------------
# Recursive Python expansion
# -----------------------------
def _expand_python_calls(project_ir: ProjectIR, project_name: str, call_list, visited=None):
    if visited is None:
        visited = set()

    children = []

    for call in call_list or []:
        resolved = _find_python_function(project_ir, call)
        if resolved is None:
            continue

        key = resolved.get("full_name") or resolved.get("name")
        if key in visited:
            node = {
                "id": key,
                "type": "python",
                "meta": {**resolved, "recursive": True},
                "children": [],
            }
            children.append(node)
            continue

        visited.add(key)

        sub_calls = resolved.get("calls", [])
        node_children = _expand_python_calls(project_ir, project_name, sub_calls, visited)

        node = {
            "id": key,
            "type": "python",
            "meta": resolved,
            "children": node_children,
        }
        children.append(node)

    return children


# -----------------------------
# Entry point
# -----------------------------
def resolve(project_ir: ProjectIR, project_name: str, trigger_name: str):
    """
    Entry point.
    Determine trigger type (JS/API/Python/HTML)
    and dispatch to the correct resolver.
    """
    # JS trigger
    js_entry = _find_js_function(project_ir, trigger_name)
    if js_entry:
        return resolve_js(project_ir, project_name, trigger_name, js_entry)

    # API trigger (by route name)
    api_entry = _find_api_route_by_name(project_ir, trigger_name)
    if api_entry:
        return resolve_api(project_ir, project_name, api_entry)

    # Python trigger (by function name)
    py_entry = _find_python_function(project_ir, trigger_name)
    if py_entry:
        return resolve_python_root(project_ir, project_name, py_entry)

    # HTML triggers would go here if present
    return {
        "id": trigger_name,
        "type": "unknown",
        "meta": {"error": "Unknown trigger"},
        "children": [],
    }


# -----------------------------
# JS → API → Python
# -----------------------------
def resolve_js(project_ir: ProjectIR, project_name: str, trigger_name: str, js_entry: dict):
    js_node = {
        "id": trigger_name,
        "type": "js",
        "meta": js_entry,
        "children": [],
    }

    api_children = []

    api_calls = js_entry.get("api_calls", [])
    if isinstance(api_calls, str):
        api_calls = [api_calls]

    for api_call_line in api_calls:
        api_entry = _find_api_route_by_path(project_ir, api_call_line)
        if not api_entry:
            continue
        api_node = resolve_api(project_ir, project_name, api_entry)
        api_children.append(api_node)

    js_node["children"] = api_children
    return js_node


def resolve_api(project_ir: ProjectIR, project_name: str, api_entry: dict):
    route_name = api_entry.get("name") or api_entry.get("route")
    api_id = route_name

    api_node = {
        "id": api_id,
        "type": "api",
        "meta": api_entry,
        "children": [],
    }

    api_calls = api_entry.get("calls", [])
    py_children = _expand_python_calls(project_ir, project_name, api_calls, visited=None)
    api_node["children"] = py_children

    return api_node


def resolve_python_root(project_ir: ProjectIR, project_name: str, py_entry: dict):
    key = py_entry.get("full_name") or py_entry.get("name")
    children = _expand_python_calls(project_ir, project_name, py_entry.get("calls", []), visited={key})

    return {
        "id": key,
        "type": "python",
        "meta": py_entry,
        "children": children,
    }
