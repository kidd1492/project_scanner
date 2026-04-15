# core/analyzers/html_analyzer.py

from bs4 import BeautifulSoup
import re
from pathlib import Path
from .base_analyzer import BaseAnalyzer
from core.ir_system.typed_ir import IREvent, IRJSFunction, IRFile

EVENT_ATTR_PATTERN = re.compile(r"^on[a-zA-Z]+$")
FUNC_CALL_PATTERN = re.compile(r"([a-zA-Z_]\w*)\s*\(")


class HTMLAnalyzer(BaseAnalyzer):
    file_type = "html"

    def analyze_file(self, file: str) -> IRFile:
        file = file.replace("\\", "/")
        source = Path(file).name
        content = Path(file).read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(content, "html.parser")

        html_events = []
        js_functions = []

        # Event attributes
        for tag in soup.find_all(True):
            for attr, value in tag.attrs.items():
                if EVENT_ATTR_PATTERN.match(attr):
                    funcs = FUNC_CALL_PATTERN.findall(value or "")
                    for func in funcs:
                        html_events.append(
                            IREvent(
                                event=attr,
                                name=func,
                                file=file,
                                source=source,
                                line=getattr(tag, "sourceline", None),
                                symbol_id=f"{source}::{func}",
                            )
                        )

        # Script blocks
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
                            file=file,
                            source=source,
                            line=getattr(script, "sourceline", None),
                            symbol_id=f"{source}::{func}",
                        )
                    )

        return IRFile(
            path=file,
            source=content,
            type="html",
            html_events=html_events,
            js_functions=js_functions,
        )

    def analyze_files(self, file_list):
        return [self.analyze_file(f) for f in file_list]
