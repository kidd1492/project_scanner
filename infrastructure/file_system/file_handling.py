# utilities/file_handling.py

import json

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def open_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# infrastructure/file_system/open_file_tool.py

from pathlib import Path

# infrastructure/file_system/file_handling.py

class OpenFileTool:
    def __call__(self, path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

