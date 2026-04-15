# core/ir_system/typed_ir_adapter.py
from typing import Dict, Any, List

from .typed_ir import (
    ProjectIR,
    IRFile,
    Route,
    IRFunction,
    IRClass,
    IRMethod,
    IREvent,
    IRJSFunction,
)


# -----------------------------
# Route
# -----------------------------
def route_from_dict(d: Dict[str, Any]) -> Route:
    return Route(
        name=d.get("name", ""),
        route=d.get("route", ""),
        args=d.get("args", []) or [],
        calls=d.get("calls", []) or [],
        returns=d.get("returns"),
        file=d.get("file", ""),
        source=d.get("source", ""),
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


# -----------------------------
# Function
# -----------------------------
def function_from_dict(d: Dict[str, Any]) -> IRFunction:
    return IRFunction(
        name=d.get("name", ""),
        args=d.get("args", []) or [],
        returns=d.get("returns"),
        calls=d.get("calls", []) or [],
        file=d.get("file", ""),
        source=d.get("source", ""),
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


# -----------------------------
# Method
# -----------------------------
def method_from_dict(d: Dict[str, Any]) -> IRMethod:
    return IRMethod(
        name=d.get("name", ""),
        args=d.get("args", []) or [],
        returns=d.get("returns"),
        calls=d.get("calls", []) or [],
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


# -----------------------------
# Class
# -----------------------------
def class_from_dict(d: Dict[str, Any]) -> IRClass:
    methods = [method_from_dict(m) for m in d.get("methods", [])]

    return IRClass(
        name=d.get("name", ""),
        methods=methods,
        file=d.get("file", ""),
        source=d.get("source", ""),
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


# -----------------------------
# HTML Event
# -----------------------------
def event_from_dict(d: Dict[str, Any]) -> IREvent:
    return IREvent(
        name=d.get("name", ""),
        handler=d.get("handler", ""),
        file=d.get("file", ""),
        source=d.get("source", ""),
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


# -----------------------------
# JS Function
# -----------------------------
def js_function_from_dict(d: Dict[str, Any]) -> IRJSFunction:
    return IRJSFunction(
        name=d.get("name", ""),
        args=d.get("args", []) or [],
        calls=d.get("calls", []) or [],
        file=d.get("file", ""),
        source=d.get("source", ""),
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


# -----------------------------
# IRFile
# -----------------------------
def file_from_dict(d: Dict[str, Any]) -> IRFile:
    return IRFile(
        path=d.get("path", ""),
        source=d.get("source", ""),
        type=d.get("type", ""),

        routes=[route_from_dict(r) for r in d.get("routes", [])],
        functions=[function_from_dict(fn) for fn in d.get("functions", [])],
        classes=[class_from_dict(cls) for cls in d.get("classes", [])],
        imports=d.get("imports", []),
        html_events=[event_from_dict(ev) for ev in d.get("html_events", [])],
        js_functions=[js_function_from_dict(js) for js in d.get("js_functions", [])],
        api_calls=d.get("api_calls", []),
    )


# -----------------------------
# ProjectIR
# -----------------------------
def project_ir_from_dict(raw: Dict[str, Any]) -> ProjectIR:
    return ProjectIR(
        project_name=raw.get("project_name", ""),
        total_files=raw.get("total_files", 0),
        root=raw.get("root", ""),
        file_types=raw.get("file_types", []),
        files=[file_from_dict(f) for f in raw.get("files", [])],
    )
