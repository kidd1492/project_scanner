from utilities.file_handling import save_json
from utilities.file_discovery import discover_files
from analyzers.base_analyzer import generate_json_reports
import os


def get_project_info(directory: str):
    file_types = discover_files(directory)
    project_name = os.path.basename(directory)
    project_directory = f"data/{project_name}"

    # If project exists, just return
    if os.path.exists(project_directory):
        save_json({"last": project_name}, "data/last_project.json")
        return {"results": "Project Exist."}

    data = {
        "project_name": project_name,
        "root": directory,
        "file_types": file_types
    }

    # Create new project folder
    os.makedirs(project_directory, exist_ok=True)
    save_json(data, f"{project_directory}/{project_name}.json")


    generate_json_reports(data, project_directory)

    # Save last opened project
    save_json({"last": project_name}, "data/last_project.json")

    return data


def get_existing_projects():
    DATA_DIR = "data"
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)
    return projects