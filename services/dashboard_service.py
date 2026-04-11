import os
from utilities.file_handling import save_json, open_json

DATA_DIR = "data"

"""TODO make functions for get_counts and get_charts"""

def get_counts():
    ...

def get_charts():
    ...


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