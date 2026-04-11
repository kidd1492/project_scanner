from utilities.file_handling import open_json
import os

DATA_DIR = "data"

def load_ir(project_name):
    project_file = os.path.join(DATA_DIR, project_name, f"{project_name}.json")
    data = open_json(project_file)
    return data.get("ir", {})

def list_files(ir):
    return ir.get("files", [])

def get_file(ir, path):
    for f in ir.get("files", []):
        if f["path"] == path:
            return f
    return None

def get_symbol_by_id(ir, symbol_id):
    for f in ir.get("files", []):
        for group in ("functions", "classes", "routes", "imports", "js_functions", "html_events"):
            for item in f.get(group, []):
                if item.get("symbol_id") == symbol_id:
                    return item
    return None

def list_triggers(ir):
    triggers = []
    for f in ir.get("files", []):
        triggers.extend(f.get("html_events", []))
        triggers.extend(f.get("js_functions", []))
        triggers.extend(f.get("routes", []))
    return triggers
