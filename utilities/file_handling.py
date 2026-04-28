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

class OpenFileTool:
    """
    Persistence abstraction for analyzers.
    Analyzers NEVER touch the filesystem directly.
    They call this tool to read file content.
    """

    def read(self, path: str) -> str:
        normalized = path.replace("\\", "/")
        p = Path(normalized)
        return p.read_text(encoding="utf-8", errors="ignore")
