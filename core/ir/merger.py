# core/ir/merger.py

from pathlib import Path

def normalize_path(path: str) -> str:
    """Normalize paths to POSIX style for consistency in IR."""
    return Path(path).as_posix()


def ensure_file_entry(ir, file_path, language, kind="source"):
    """
    Ensure a file entry exists in IR["files"].
    Returns the file entry dict.
    """
    file_path = normalize_path(file_path)

    for f in ir["files"]:
        if f["path"] == file_path:
            return f

    entry = {
        "path": file_path,
        "language": language,
        "kind": kind,
        "functions": [],
        "classes": [],
        "routes": [],
        "triggers": [],
        "api_calls": [],
    }

    ir["files"].append(entry)
    return entry


def merge_trigger(file_entry, trigger):
    file_entry["triggers"].append(trigger)


def merge_js_function(file_entry, func):
    file_entry["functions"].append(func)


def merge_api_call(file_entry, api_call):
    file_entry["api_calls"].append(api_call)


def merge_route(file_entry, route):
    file_entry["routes"].append(route)


def merge_class(file_entry, cls):
    file_entry["classes"].append(cls)


def merge_python_function(file_entry, func):
    file_entry["functions"].append(func)
