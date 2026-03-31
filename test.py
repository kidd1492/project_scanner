import re
from analyzers.helpers import open_json


# -----------------------------
# Normalize JS fetch() path
# -----------------------------
def normalize_js_api_call(api_call):
    if not api_call:
        return ""

    # Extract the first quoted/backtick string inside fetch(...)
    m = re.search(r'fetch\s*\(\s*[\'"`]([^\'"`]+)[\'"`]', api_call)
    if not m:
        return ""

    path = m.group(1)

    # Remove query params
    path = path.split("?")[0]

    # Ensure leading slash
    if not path.startswith("/"):
        path = "/" + path

    # Remove blueprint prefixes
    path = re.sub(r'^/(chat_route|ingestion|research|retrieval)', '', path)

    # Remove trailing slash
    if path.endswith("/"):
        path = path[:-1]

    return path


# -----------------------------
# Convert Flask route to regex
# -----------------------------
def route_to_regex(route):
    """
    Convert Flask route with <param> into a regex.
    Example:
        /add_wiki/<term> -> ^/add_wiki/[^/]+$
    """
    pattern = re.sub(r"<[^>]+>", r"[^/]+", route)
    return "^" + pattern + "$"


# -----------------------------
# Find JS function by trigger
# -----------------------------
def find_js_function(trigger_name):
    js_data = open_json("data/js.json")
    func_name = trigger_name.split("(")[0]

    for entry in js_data:
        if entry["function"] == func_name:
            return entry

    return None


# -----------------------------
# Match JS fetch → API route
# -----------------------------
def find_api_route(api_call_line):
    api_data = open_json("data/api.json")
    js_path = normalize_js_api_call(api_call_line)

    for route in api_data:
        route_regex = route_to_regex(route["route"])
        if re.match(route_regex, js_path):
            return route

    return None


# -----------------------------
# TEST
# -----------------------------
html = "runQuery()"
print("Trigger:", html, "\n")

js = find_js_function(html)
print("JS Entry:", js, "\n")

api = find_api_route(js.get("api_calls"))
print("Matched API Route:", api, "\n")
