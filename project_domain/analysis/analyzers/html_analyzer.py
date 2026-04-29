# domain/analysis/analyzers/html_analyzer.py

from pathlib import Path
import re
from bs4 import BeautifulSoup

from .base_analyzer import BaseAnalyzer
from project_domain.analysis.analysis_objects import IREvent, IRJSFunction
from project_domain.analysis.file_object.ir_file import IRFile


EVENT_ATTR_PATTERN = re.compile(r"^on[a-zA-Z]+$")
FUNC_CALL_PATTERN = re.compile(r"([a-zA-Z_]\w*)\s*\(")


class HTMLAnalyzer(BaseAnalyzer):
    file_type = "html"

    def analyze_file(self, path: str, content: str) -> IRFile:
        """
        CAP‑correct:
        - receives path + content (already opened)
        - does NOT read files
        - returns IRFile with html_events + js_functions
        """

        # Normalize path
        path = path.replace("\\", "/")
        p = Path(path)
        source_name = p.name

        # Parse HTML
        soup = BeautifulSoup(content, "html.parser")

        html_events: list[IREvent] = []
        js_functions: list[IRJSFunction] = []

        # ---------------------------------------------------------
        # Extract HTML event attributes (onclick, onsubmit, etc.)
        # ---------------------------------------------------------
        for tag in soup.find_all(True):
            for attr, value in tag.attrs.items():
                if EVENT_ATTR_PATTERN.match(attr):
                    funcs = FUNC_CALL_PATTERN.findall(value or "")
                    for func in funcs:
                        html_events.append(
                            IREvent(
                                event=attr,
                                name=func,
                                file=path,
                                source=source_name,
                                line=getattr(tag, "sourceline", None),
                                symbol_id=f"{source_name} :: {func}",
                            )
                        )

        # ---------------------------------------------------------
        # Extract inline <script> JS functions
        # ---------------------------------------------------------
        for script in soup.find_all("script"):
            if script.string:
                js_code = script.string
                funcs = FUNC_CALL_PATTERN.findall(js_code)
                for func in funcs:
                    js_functions.append(
                        IRJSFunction(
                            name=func,
                            args=[],
                            calls=[],
                            api_call="",
                            file=path,
                            source=source_name,
                            line=getattr(script, "sourceline", None),
                            symbol_id=f"{source_name} :: {func}",
                        )
                    )

        # ---------------------------------------------------------
        # Return IRFile (your exact structure)
        # ---------------------------------------------------------
        return IRFile(
            path=path,
            source=content,
            type="html",
            routes=[],
            functions=[],
            classes=[],
            imports=[],
            html_events=html_events,
            js_functions=js_functions,
            api_calls=[],
        )
