def resolve(ir, trigger_name):
    """
    Entry point.
    Determine trigger type (JS/API/Python/HTML)
    and dispatch to the correct resolver.
    """
    # Try JS
    js_entry = _find_in_files(ir, "js_functions", trigger_name)
    if js_entry:
        return resolve_js(ir, trigger_name)

    # Try API route
    api_entry = _find_in_files(ir, "routes", trigger_name)
    if api_entry:
        return resolve_api(ir, trigger_name)

    # Try Python function
    py_entry = _find_in_files(ir, "functions", trigger_name)
    if py_entry:
        return resolve_python(ir, trigger_name)

    # Try HTML event
    html_entry = _find_in_files(ir, "html_events", trigger_name)
    if html_entry:
        return resolve_html(ir, trigger_name)

    return {"id": trigger_name, "type": "unknown", "meta": {"error": "Unknown trigger"}, "children": []}


def _find_in_files(ir, key, name):
    """Search all files for an entry with given key and name."""
    for f in ir.get("files", []):
        for item in f.get(key, []):
            if item.get("name") == name:
                # Attach file path as meta
                meta = dict(item)
                meta["file"] = f.get("path")
                return meta
    return None


def resolve_js(ir, js_name, visited=None):
    """
    JS function -> (future) API calls -> Python calls.
    For now, just return a single node with metadata.
    """
    if visited is None:
        visited = set()
    if js_name in visited:
        return {"id": js_name, "type": "js", "meta": {"cycle": True}, "children": []}
    visited.add(js_name)

    meta = _find_in_files(ir, "js_functions", js_name) or {}
    return {
        "id": js_name,
        "type": "js",
        "meta": meta,
        "children": [],
    }


def resolve_api(ir, route_name, visited=None):
    """
    API route -> (future) Python function.
    For now, just return a single node with metadata.
    """
    if visited is None:
        visited = set()
    if route_name in visited:
        return {"id": route_name, "type": "api", "meta": {"cycle": True}, "children": []}
    visited.add(route_name)

    meta = _find_in_files(ir, "routes", route_name) or {}
    return {
        "id": route_name,
        "type": "api",
        "meta": meta,
        "children": [],
    }


def resolve_python(ir, function_name, visited=None):
    """
    Python function -> (future) internal calls.
    For now, just return a single node with metadata.
    """
    if visited is None:
        visited = set()
    if function_name in visited:
        return {"id": function_name, "type": "python", "meta": {"cycle": True}, "children": []}
    visited.add(function_name)

    meta = _find_in_files(ir, "functions", function_name) or {}
    return {
        "id": function_name,
        "type": "python",
        "meta": meta,
        "children": [],
    }


def resolve_html(ir, event_name, visited=None):
    """
    HTML event -> (future) JS function.
    For now, just return a single node with metadata.
    """
    if visited is None:
        visited = set()
    if event_name in visited:
        return {"id": event_name, "type": "html", "meta": {"cycle": True}, "children": []}
    visited.add(event_name)

    meta = _find_in_files(ir, "html_events", event_name) or {}
    return {
        "id": event_name,
        "type": "html",
        "meta": meta,
        "children": [],
    }
