import os
from utilities.file_handling import open_json, save_json

def embed_ir_into_project_json(project_dir, project_name, ir):
    project_json_path = os.path.join(project_dir, f"{project_name}.json")
    project_data = open_json(project_json_path)
    project_data["ir"] = ir
    save_json(project_data, project_json_path)
