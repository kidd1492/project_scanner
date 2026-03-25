import os
import json

def analyze_project(directory: str, output_file="data/project.json"):
    allowed_extensions = [
        ".py", ".html", ".js", ".md", ".txt", ".db",
        ".css", ".rst", ".yml"
    ]
    ignored_directories = [".git", "env", "venv", "__pycache__"]

    categorized = {}
    total_files = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        for file in files:
            total_files += 1

            if any(file.endswith(ext) for ext in allowed_extensions):
                ext = file.split('.')[-1]
                full_path = os.path.abspath(os.path.join(root, file))
                categorized.setdefault(ext, []).append(full_path)

    file_types = [
        {"type": ext, "count": len(paths), "files": paths}
        for ext, paths in categorized.items()
    ]

    data = {
        "project_name": os.path.basename(directory),
        "root": directory,
        "total_files": total_files,
        "file_types": file_types
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return data
