import re


def _get_files(ir):
    return ir.get("ir", {}).get("files", [])


# -----------------------------
# Helpers from old system
# -----------------------------
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
# IR search helpers
# -----------------------------
def _find_js_function(ir, trigger_name):
    files = _get_files(ir)
    func_name = trigger_name.split("(")[0]

    for f in files:
        for fn in f.get("js_functions", []):
            if fn.get("name") == func_name:
                meta = dict(fn)
                meta["file"] = f.get("path")
                return meta
    return None


def _find_api_route_by_name(ir, route_name):
    files = _get_files(ir)
    for f in files:
        for r in f.get("routes", []):
            if r.get("name") == route_name:
                meta = dict(r)
                meta["file"] = f.get("path")
                return meta
    return None


def _find_api_route_by_path(ir, js_api_call_line):
    files = _get_files(ir)
    js_path = normalize_js_api_call(js_api_call_line)
    if not js_path:
        return None

    for f in files:
        for r in f.get("routes", []):
            route_pattern = r.get("route")
            if not route_pattern:
                continue
            route_regex = route_to_regex(route_pattern)
            if re.match(route_regex, js_path):
                meta = dict(r)
                meta["file"] = f.get("path")
                return meta
    return None


def _find_python_function(ir, call_name):
    files = _get_files(ir)
    short = call_name.split(".")[-1]

    # Free functions
    for f in files:
        for fn in f.get("functions", []):
            if fn.get("name") == short:
                meta = dict(fn)
                meta["file"] = f.get("path")
                meta["full_name"] = call_name
                meta["kind"] = "function"
                return meta

    # Class methods
    for f in files:
        for cls in f.get("classes", []):
            cls_name = cls.get("name") or cls.get("class")
            for m in cls.get("methods", []):
                m_name = m.get("name") or m.get("method")
                if m_name == short:
                    meta = dict(m)
                    meta["file"] = f.get("path")
                    meta["class"] = cls_name
                    meta["full_name"] = call_name
                    meta["kind"] = "method"
                    return meta

    return None


# -----------------------------
# Recursive Python expansion
# -----------------------------
def _expand_python_calls(ir, project_name, call_list, visited=None):
    if visited is None:
        visited = set()

    children = []

    for call in call_list or []:
        resolved = _find_python_function(ir, call)
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
        node_children = _expand_python_calls(ir, project_name, sub_calls, visited)

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
def resolve(ir, project_name, trigger_name):
    """
    Entry point.
    Determine trigger type (JS/API/Python/HTML)
    and dispatch to the correct resolver.
    """
    # JS trigger
    js_entry = _find_js_function(ir, trigger_name)
    if js_entry:
        return resolve_js(ir, project_name, trigger_name, js_entry)

    # API trigger (by route name)
    api_entry = _find_api_route_by_name(ir, trigger_name)
    if api_entry:
        return resolve_api(ir, project_name, api_entry)

    # Python trigger (by function name)
    py_entry = _find_python_function(ir, trigger_name)
    if py_entry:
        return resolve_python_root(ir, project_name, py_entry)

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
def resolve_js(ir, project_name, trigger_name, js_entry):
    """
    JS function -> API calls -> Python calls.
    Mirrors old build_full_trace behavior.
    """
    js_node = {
        "id": trigger_name,
        "type": "js",
        "meta": js_entry,
        "children": [],
    }

    api_children = []

    # Old system used js_entry["api_calls"] (string or list)
    api_calls = js_entry.get("api_calls", [])
    if isinstance(api_calls, str):
        api_calls = [api_calls]

    for api_call_line in api_calls:
        api_entry = _find_api_route_by_path(ir, api_call_line)
        if not api_entry:
            continue
        api_node = resolve_api(ir, project_name, api_entry)
        api_children.append(api_node)

    js_node["children"] = api_children
    return js_node


def resolve_api(ir, project_name, api_entry):
    """
    API route -> Python function(s).
    """
    route_name = api_entry.get("name") or api_entry.get("route")
    api_id = route_name

    api_node = {
        "id": api_id,
        "type": "api",
        "meta": api_entry,
        "children": [],
    }

    # Old system: api_entry["calls"] = list of python call names
    api_calls = api_entry.get("calls", [])
    py_children = _expand_python_calls(ir, project_name, api_calls, visited=None)
    api_node["children"] = py_children

    return api_node


def resolve_python_root(ir, project_name, py_entry):
    """
    Python trigger used directly as root.
    """
    key = py_entry.get("full_name") or py_entry.get("name")
    children = _expand_python_calls(ir, project_name, py_entry.get("calls", []), visited={key})

    return {
        "id": key,
        "type": "python",
        "meta": py_entry,
        "children": children,
    }
