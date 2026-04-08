import os
from utilities.file_handling import save_json

def get_existing_projects():
    DATA_DIR = "data"
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)
    return projects


def initialize_project(directory: str):
    project_name = os.path.basename(directory)
    project_dir = f"data/{project_name}"

    if _project_exists(project_dir):
        return _handle_existing_project(project_name)

    _initialize_project_directory(project_dir)
    return {
        "results": "OK",
        "project_name": project_name,
        "project_dir": project_dir
    }

def _project_exists(project_dir: str) -> bool:
    return os.path.exists(project_dir)


def _handle_existing_project(project_name: str):
    save_json({"last": project_name}, "data/last_project.json")
    return {"results": "Project Exist."}

def _initialize_project_directory(project_dir: str):
    os.makedirs(project_dir, exist_ok=True)