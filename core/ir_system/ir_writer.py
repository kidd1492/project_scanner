import os
from utilities.file_handling import save_json


def save_project_ir(project_dir, project_name, ir, metadata):
    data = {
        "project_name":metadata["project_name"],
        "total_files":metadata["total_files"],
        "root":metadata["root"],
        "file_types":metadata["file_types"],
        "ir":ir

    }
    project_json_path = os.path.join(project_dir, f"{project_name}.json")
    save_json(data, project_json_path)