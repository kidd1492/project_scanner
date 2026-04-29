# utilities/file_discovery.py

import os

def discover_files(directory: str):
    allowed_extensions = [
        ".py", ".html", ".js", ".md", ".txt", ".db",
        ".css", ".rst", ".yml"
    ]
    ignored_directories = [".git", "env", "venv", "__pycache__"]

    file_list = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                full_path = os.path.abspath(os.path.join(root, file))
                full_path = full_path.replace("\\", "/")
                file_list.append(full_path)

    return file_list
