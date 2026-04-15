# core/ir_system/builder.py

import os
from utilities.file_discovery import discover_files
from core.analyzers.python_analyzer import PythonAnalyzer
from core.analyzers.js_analyzer import JSAnalyzer
from core.analyzers.html_analyzer import HTMLAnalyzer
from core.ir_system.typed_ir import ProjectIR


def build_project_ir(directory: str) -> ProjectIR:
    file_types, _ = discover_files(directory)

    py_files = []
    js_files = []
    html_files = []

    for ft in file_types:
        if ft["type"] == "py":
            py_files.extend(ft["files"])
        elif ft["type"] == "js":
            js_files.extend(ft["files"])
        elif ft["type"] == "html":
            html_files.extend(ft["files"])

    ir_files = []

    # Python
    py_analyzer = PythonAnalyzer()
    ir_files += [py_analyzer.analyze_file(f) for f in py_files]

    # JS
    js_analyzer = JSAnalyzer()
    ir_files += [js_analyzer.analyze_file(f) for f in js_files]

    # HTML
    html_analyzer = HTMLAnalyzer()
    ir_files += [html_analyzer.analyze_file(f) for f in html_files]

    return ProjectIR(
        project_name=os.path.basename(directory),
        total_files=len(ir_files),
        root=directory,
        file_types=file_types,
        files=ir_files,
    )
