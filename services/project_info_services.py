from analyzers.helpers import analyze_project, save_json
from analyzers.base_analyzer import generate_json_reports
import os


def get_project_info(directory: str):
    data = analyze_project(directory)
    project_directory = f"data/{data['project_name']}"

    # If project exists, just return
    if os.path.exists(project_directory):
        save_json({"last": data["project_name"]}, "data/last_project.json")
        return {"results": "Project Exist."}

    # Create new project folder
    os.makedirs(project_directory, exist_ok=True)
    save_json(data, f"{project_directory}/{data['project_name']}.json")
    generate_json_reports(data, project_directory)

    # Save last opened project
    save_json({"last": data["project_name"]}, "data/last_project.json")

    return data


