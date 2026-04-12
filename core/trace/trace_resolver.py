def resolve(ir, trigger_name):
    """
    Entry point.
    Determine trigger type (JS/API/Python/HTML)
    and dispatch to the correct resolver.
    """
    if trigger_name in ir["js_functions"]:
        return resolve_js(ir, trigger_name)

    if trigger_name in ir["routes"]:
        return resolve_api(ir, trigger_name)

    if trigger_name in ir["functions"]:
        return resolve_python(ir, trigger_name)

    if trigger_name in ir["html_events"]:
        return resolve_html(ir, trigger_name)

    return {"error": "Unknown trigger"}


def resolve_js(ir, js_name, visited=None):
    """
    JS function → API calls → Python calls
    """
    # returns:
    # { "id": "...", "type": "js", "children": [...] }
    pass


def resolve_api(ir, route_name, visited=None):
    """
    API route → Python function
    """
    pass


def resolve_python(ir, function_name, visited=None):
    """
    Python function → internal calls
    """
    pass


def resolve_html(ir, event_name, visited=None):
    """
    HTML event → JS function
    """
    pass
