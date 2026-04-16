# core/analyzers/js_analyzer.py

import re
from pathlib import Path
from .base_analyzer import BaseAnalyzer
from core.ir_system.typed_ir import IRJSFunction, IRFile

FUNCTION_PATTERN = re.compile(
    r"""
    function\s+(\w+)\s*\(
    |
    const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{
    |
    (?:let|var)\s+(\w+)\s*=\s*function\s*\(
    |
    async\s+function\s+(\w+)\s*\(
    """,
    re.VERBOSE
)

API_CALL_PATTERN = re.compile(r"fetch\s*\(")


class JSAnalyzer(BaseAnalyzer):
    file_type = "js"

    def analyze_file(self, file: str) -> IRFile:
        file = file.replace("\\", "/")
        source = Path(file).name
        content = Path(file).read_text(encoding="utf-8", errors="ignore")

        js_functions = []

        for match in FUNCTION_PATTERN.finditer(content):
            func_name = next((g for g in match.groups() if g), None)
            start_index = match.end()

            func_body = self._extract_function_body(content, start_index)
            api_call = self._find_fetch(func_body)

            js_functions.append(
                IRJSFunction(
                    name=func_name,
                    args=[],
                    calls=[],
                    api_call=api_call,
                    file=file,
                    source=source,
                    line=content.count("\n", 0, match.start()) + 1,
                    symbol_id=f"{source}::{func_name}",
                )
            )

        return IRFile(
            path=file,
            source=content,
            type="js",
            js_functions=js_functions,
        )

    def analyze_files(self, file_list):
        return [self.analyze_file(f) for f in file_list]

    def _extract_function_body(self, content, start_index):
        brace_count = 0
        body = []
        started = False

        for i in range(start_index, len(content)):
            c = content[i]

            if c == "{":
                brace_count += 1
                started = True

            if started:
                body.append(c)

            if c == "}":
                brace_count -= 1
                if brace_count == 0 and started:
                    break

        return "".join(body)

    def _find_fetch(self, func_body):
        for line in func_body.splitlines():
            if API_CALL_PATTERN.search(line):
                return line.strip()
        return ""
