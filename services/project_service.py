import os
from utilities.file_handling import open_json
from core.project_system.project_generator import scan_project_files


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
    return project_data


def generate_project_data(directory):
    return scan_project_files(directory)
