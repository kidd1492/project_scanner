# core/analyzers/html_analyzer.py

from bs4 import BeautifulSoup
import re
from pathlib import Path
from .base_analyzer import BaseAnalyzer

EVENT_ATTR_PATTERN = re.compile(r"^on[a-zA-Z]+$")
FUNC_CALL_PATTERN = re.compile(r"([a-zA-Z_]\w*)\s*\(")

class HTMLAnalyzer(BaseAnalyzer):
    file_type = "html"

    def analyze_files(self, file_list):
        results = []

        for file in file_list:
            file = file.replace("\\", "/")
            source = file.split("/")[-1]
            content = Path(file).read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            # 1. Extract event attributes (onclick, onchange, etc.)
            for tag in soup.find_all(True):
                for attr, value in tag.attrs.items():
                    if EVENT_ATTR_PATTERN.match(attr):
                        funcs = FUNC_CALL_PATTERN.findall(value or "")
                        for func in funcs:
                            results.append({
                                "type": "html_event",
                                "event": attr,
                                "name": func,
                                "args": [],
                                "calls": [],
                                "file": file,
                                "source": source,
                                "line": getattr(tag, "sourceline", None)
                            })

            # 2. Extract JS inside <script> tags
            for script in soup.find_all("script"):
                if script.string:
                    js_code = script.string
                    funcs = FUNC_CALL_PATTERN.findall(js_code)
                    for func in funcs:
                        results.append({
                            "type": "html_script_function",
                            "event": "script_block",
                            "name": func,
                            "args": [],
                            "calls": [],
                            "file": file,
                            "source": source,
                            "line": getattr(script, "sourceline", None)
                        })

        return results
