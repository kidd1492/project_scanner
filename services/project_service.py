import os
from utilities.file_handling import save_json, open_json

DATA_DIR = "data"

def get_existing_projects():
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)
    return projects


def load_project(project_name):
    project_dir = os.path.join(DATA_DIR, project_name)
    project_file = os.path.join(project_dir, f"{project_name}.json")

    if not os.path.exists(project_file):
        return f"Project '{project_name}' not found.", 404

    project_data = open_json(project_file)
    save_json({"last": project_name}, "data/last_project.json")
    return project_data


def load_analysis_type(project_name, analysis_type):
    project_dir = os.path.join(DATA_DIR, project_name)
    file_path = os.path.join(project_dir, f"{analysis_type}.json")

    if not os.path.exists(file_path):
        return []
    data = open_json(file_path)
    return data


def load_last_dashboard():
    last_file = os.path.join(DATA_DIR, "last_project.json")
    if not os.path.exists(last_file):
        return "no_file"
    last = open_json(last_file).get("last")
    if not last:
        return "no_file"
    return last


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