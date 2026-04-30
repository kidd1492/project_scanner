# infrastructure/file_system/file_discovery.py

import os

class FileDiscovery:
    def __init__(self):
        self.allowed_extensions = [
            ".py", ".html", ".js", ".md", ".txt", ".db",
            ".css", ".rst", ".yml"
        ]
        self.ignored_directories = [".git", "env", "venv", "__pycache__"]

    def __call__(self, directory: str) -> list[str]:
        file_list = []

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in self.ignored_directories]

            for file in files:
                if any(file.endswith(ext) for ext in self.allowed_extensions):
                    full_path = os.path.abspath(os.path.join(root, file))
                    full_path = full_path.replace("\\", "/")
                    file_list.append(full_path)

        return file_list
