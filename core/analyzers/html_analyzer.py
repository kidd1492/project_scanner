from bs4 import BeautifulSoup
import re
from pathlib import Path

EVENT_ATTR_PATTERN = re.compile(r"^on[a-zA-Z]+$")   # onclick, onchange, etc.
FUNC_CALL_PATTERN = re.compile(r"([a-zA-Z_]\w*)\s*\(")

class HTMLAnalyzer:
    def __init__(self):
        self.file_type = "html"
        self.results = []

    def analyze_files(self, file_list):
        self.results = []

        for file in file_list:
            content = Path(file).read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(content, "html.parser")

            # 1. Extract event attributes
            for tag in soup.find_all(True):
                for attr, value in tag.attrs.items():
                    if EVENT_ATTR_PATTERN.match(attr):
                        funcs = FUNC_CALL_PATTERN.findall(value or "")
                        for func in funcs:
                            self.results.append({
                                "file": file,
                                "file_type": self.file_type,
                                "event": attr,
                                "function": func,
                                "source": file.split('/')[-1]
                            })

            # 2. Extract JS inside <script> tags
            for script in soup.find_all("script"):
                if script.string:
                    js_code = script.string
                    funcs = FUNC_CALL_PATTERN.findall(js_code)
                    for func in funcs:
                        self.results.append({
                            "file": file,
                            "file_type": self.file_type,
                            "event": "script_block",
                            "function": func,
                            "source": file.split('/')[-1]
                        })

        return self.results
