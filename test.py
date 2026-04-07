import re, json
from utilities.file_handling import open_json


# -----------------------------
# Normalize JS fetch() path
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


# -----------------------------
# Convert Flask route to regex
# -----------------------------
def route_to_regex(route):
    pattern = re.sub(r"<[^>]+>", r"[^/]+", route)
    return "^" + pattern + "$"


# -----------------------------
# Find JS function by trigger
# -----------------------------
def find_js_function(trigger_name, project_name):
    js_data = open_json(f"data/{project_name}/js.json")
    func_name = trigger_name.split("(")[0]

    for entry in js_data:
        if entry["function"] == func_name:
            return entry

    return None


# -----------------------------
# Match JS fetch → API route
# -----------------------------
def find_api_route(api_call_line, project_name):
    api_data = open_json(f"data/{project_name}/api.json")
    js_path = normalize_js_api_call(api_call_line)

    for route in api_data:
        route_regex = route_to_regex(route["route"])
        if re.match(route_regex, js_path):
            return route

    return None


# -----------------------------
# Resolve a Python call (developer functions only)
# -----------------------------
def resolve_python_call(call_name, project_name):
    functions = open_json(f"data/{project_name}/functions.json")
    classes = open_json(f"data/{project_name}/classes.json")

    short = call_name.split(".")[-1]

    # Free functions
    for f in functions:
        if f["function"] == short:
            return {
                "type": "function",
                "name": short,
                "full_name": call_name,
                "file": f.get("file"),
                "args": f.get("args"),
                "returns": f.get("returns"),
                "calls": f.get("calls", [])
            }

    # Class methods
    for cls in classes:
        for m in cls["methods"]:
            if m["method"] == short:
                return {
                    "type": "method",
                    "name": short,
                    "full_name": call_name,
                    "class": cls["class"],
                    "file": cls["file"],
                    "args": m.get("args"),
                    "returns": m.get("returns"),
                    "calls": m.get("calls", [])
                }

    # Unknown → IGNORE
    return None


# -----------------------------
# Recursively expand calls (developer functions only)
# -----------------------------
def expand_calls_recursively(call_list, project_name, visited=None):
    if visited is None:
        visited = set()

    expanded = []

    for call in call_list:
        resolved = resolve_python_call(call, project_name)

        # Skip unknown calls entirely
        if resolved is None:
            continue

        key = resolved["full_name"]
        if key in visited:
            resolved["recursive"] = True
            resolved["children"] = []
            expanded.append(resolved)
            continue

        visited.add(key)

        child_calls = resolved.get("calls", [])
        resolved["children"] = expand_calls_recursively(child_calls, project_name, visited)

        expanded.append(resolved)

    return expanded


# -----------------------------
# Build full trace object
# -----------------------------
def build_full_trace(trigger_name, project_name):
    trace = {
        "trigger": trigger_name,
        "js": None,
        "api": None,
        "python": []
    }

    # JS
    js_entry = find_js_function(trigger_name, project_name)
    trace["js"] = js_entry

    if not js_entry:
        return trace

    # API
    api_entry = find_api_route(js_entry.get("api_calls"), project_name)
    trace["api"] = api_entry

    if not api_entry:
        return trace

    # Python recursive expansion
    api_calls = api_entry.get("calls", [])
    trace["python"] = expand_calls_recursively(api_calls, project_name)

    return trace


def trace_to_mermaid(trace):
    lines = ["flowchart TD"]

    def walk(node, parent_id=None, counter=[0]):
        counter[0] += 1
        node_id = f"N{counter[0]}"

        label = node["name"]
        args = node.get("args", [])
        if args:
            label += f"({', '.join(args)})"

        lines.append(f'    {node_id}["{label}"]')

        if parent_id:
            lines.append(f"    {parent_id} --> {node_id}")

        for child in node.get("children", []):
            walk(child, node_id)

    # Top-level Python calls
    for root in trace["python"]:
        walk(root)

    return "\n".join(lines)



if __name__ == "__main__":
    project_name = "expert_in_a_box"
    trigger = "uploadFile()"
    trace = build_full_trace(trigger, project_name)
    print(trace)
    #mermaid = trace_to_mermaid(trace)
    #print(json.dumps(trace, indent=4))
    #print(mermaid)
