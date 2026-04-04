from utilities.file_handling import save_json, open_json
from utilities.file_discovery import discover_files
from analyzers.base_analyzer import generate_json_reports
import os
import matplotlib
matplotlib.use("Agg")  # Non-GUI backend for server environments
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
    analysis_counts = get_counts(project_name)
    total_files = get_total_files(file_types)
    file_pie_chat(file_types, project_name)
    analysis_bar_chart(analysis_counts, project_name)


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


def analysis_bar_chart(analysis_counts, project_name):
    """
    Creates a horizontal bar chart for analysis counts and saves it
    to the project's static image directory.
    """

    # Extract labels and values
    labels = list(analysis_counts.keys())
    values = list(analysis_counts.values())

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values, color="#4a90e2")
    plt.xlabel("Count")
    plt.title("Analysis Summary")

    # Add value labels on bars
    for index, value in enumerate(values):
        plt.text(value + 0.1, index, str(value), va='center')

    # Save chart
    project_image_directory = f"web_app/static/projects/{project_name}"
    os.makedirs(project_image_directory, exist_ok=True)
    plt.savefig(f"{project_image_directory}/analysis.png", bbox_inches='tight')

    plt.close()
