from utilities.file_handling import save_json
from utilities.file_discovery import discover_files
from analyzers.base_analyzer import generate_json_reports
import os
import matplotlib.pyplot as plt

def ingest_project(directory: str):
    project_name = os.path.basename(directory)
    project_directory = f"data/{project_name}"

    if os.path.exists(project_directory):
        save_json({"last": project_name}, "data/last_project.json")
        return {"results": "Project Exist."}
    
    os.makedirs(project_directory, exist_ok=True)
    file_types = discover_files(directory)
    generate_json_reports(file_types, project_directory)
    total_files = get_total_files(file_types)
    file_pie_chat(file_types, project_name)

    data = {
        "project_name": project_name,
        "total_files": total_files,
        "root": directory,
        "file_types": file_types,
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


def get_total_files(file_types):
    total_files = 0
    for type in file_types:
        total_files += type.get("count")
    return total_files


def file_pie_chat(file_types, project_name):
    file_type_sizes = []
    file_type_labels = []

    for type in file_types:
        file_type_labels.append(type['type'])
        file_type_sizes.append(type['count'])

    plt.figure(figsize=(8, 8))
    plt.pie(
        file_type_sizes,
        labels=file_type_labels,
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title("Percentage of File Types Analyzed")

    # Save instead of show
    project_image_directory = f"web_app/static/projects/{project_name}"
    os.makedirs(project_image_directory, exist_ok=True)
    plt.savefig(f"{project_image_directory}/chat.png", bbox_inches='tight')


    # Close the figure so it doesn't display or leak memory
    plt.close()
