# infrastructure/file_system/file_reader.py

import json

class FileReader:
    """Environment-dependent file reading/writing tool.
    Pure infrastructure. Swappable. Injectable. CAP‑aligned."""
    
    def read_text(self, path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def read_json(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_json(self, path: str, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
