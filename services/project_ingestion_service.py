from utilities.file_handling import save_json, open_json
from utilities.file_discovery import discover_files
from utilities import chart_generator
from analyzers.base_analyzer import generate_json_reports
import os


def ingest_project(directory: str):
    project_name = os.path.basename(directory)
    project_directory = f"data/{project_name}"

    if os.path.exists(project_directory): 
        save_json({"last": project_name}, "data/last_project.json")
        return {"results": "Project Exist."}
    
    os.makedirs(project_directory, exist_ok=True)

    file_types, total_files = discover_files(directory)
    generate_json_reports(file_types, project_directory)

    analysis_counts = get_counts(project_name)

    chart_generator.file_pie_chat(file_types, project_name)
    chart_generator.analysis_bar_chart(analysis_counts, project_name)


    data = {
        "project_name": project_name,
        "total_files": total_files,
        "root": directory,
        "file_types": file_types,
        "analysis_counts": analysis_counts,
    }

    save_json(data, f"{project_directory}/{project_name}.json")
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


def get_counts(project_name):
    """
    Opens all analysis JSON files inside data/<project_name>/ 
    and returns a dictionary of item counts.
    """

    project_dir = os.path.join("data", project_name)

    summary = {
        "html_triggers": 0,
        "js_functions": 0,
        "api_routes": 0,
        "classes": 0,
        "python_functions": 0
    }

    # Map filenames → summary keys
    file_map = {
        "html.json": "html_triggers",
        "js.json": "js_functions",
        "api.json": "api_routes",
        "classes.json": "classes",
        "functions.json": "python_functions"
    }

    for filename, key in file_map.items():
        file_path = os.path.join(project_dir, filename)

        if os.path.exists(file_path):
            data = open_json(file_path)

            # Ensure it's a list before counting
            if isinstance(data, list):
                summary[key] = len(data)
            else:
                summary[key] = 0

    return summary
