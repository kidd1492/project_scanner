import os

def discover_files(directory: str):
    allowed_extensions = [
        ".py", ".html", ".js", ".md", ".txt", ".db",
        ".css", ".rst", ".yml"
    ]
    ignored_directories = [".git", "env", "venv", "__pycache__"]

    categorized = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                ext = file.split('.')[-1]
                full_path = os.path.abspath(os.path.join(root, file))
                categorized.setdefault(ext, []).append(full_path)

    file_types = [
        {"type": ext, "count": len(paths), "files": paths}
        for ext, paths in categorized.items()
    ]
    return file_types