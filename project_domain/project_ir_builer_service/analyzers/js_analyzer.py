# core/analyzers/js_analyzer.py

import re
from pathlib import Path

from .base_analyzer import BaseAnalyzer
from project_domain.project_ir_builer_service.analysis_objects import IRJSFunction
from project_domain.project_ir_builer_service.analysis_objects.ir_file import IRFile


# Match several JS function forms:
#   function name(...) { ... }
#   const name = (...) => { ... }
#   let name = function(...) { ... }
#   async function name(...) { ... }
FUNCTION_PATTERN = re.compile(
    r"""
    function\s+(\w+)\s*\(              # function name(...) {
    |
    const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{   # const name = (...) => {
    |
    (?:let|var)\s+(\w+)\s*=\s*function\s*\(   # let name = function(...) {
    |
    async\s+function\s+(\w+)\s*\(             # async function name(...) {
    """,
    re.VERBOSE,
)

# Extract only the fetch(...) call text if present
FETCH_CALL_PATTERN = re.compile(r"fetch\s*\([^)]*\)")


class JSAnalyzer(BaseAnalyzer):
    file_type = "js"

    def analyze_file(self, path: str, content: str) -> IRFile:
        # Normalize path
        file = file.replace("\\", "/")
        path = Path(file)
        source_name = path.name
        
        js_functions: list[IRJSFunction] = []

        for match in FUNCTION_PATTERN.finditer(content):
            func_name = next((g for g in match.groups() if g), None)
            if not func_name:
                continue

            start_index = match.end()
            func_body = self._extract_function_body(content, start_index)
            api_call = self._find_fetch(func_body)

            line_number = content.count("\n", 0, match.start()) + 1

            js_functions.append(
                IRJSFunction(
                    name=func_name,
                    args=[],
                    calls=[],
                    api_call=api_call or "",
                    file=str(path),
                    source=source_name,
                    line=line_number,
                    symbol_id=f"{source_name} :: {func_name}",
                )
            )

        return IRFile(
            path=str(path),
            source=content,
            type="js",
            routes=[],
            functions=[],
            classes=[],
            imports=[],
            html_events=[],
            js_functions=js_functions,
            api_calls=[],
        )

    def _extract_function_body(self, content: str, start_index: int) -> str:
        brace_count = 0
        body_chars: list[str] = []
        started = False

        for i in range(start_index, len(content)):
            c = content[i]
            if c == "{":
                brace_count += 1
                started = True
            if started:
                body_chars.append(c)
            if c == "}":
                brace_count -= 1
                if brace_count == 0 and started:
                    break

        return "".join(body_chars)

    def _find_fetch(self, func_body: str) -> str | None:
        for line in func_body.splitlines():
            match = FETCH_CALL_PATTERN.search(line)
            if match:
                return match.group(0)
        return None
