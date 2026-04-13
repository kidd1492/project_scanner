import os
from utilities.file_handling import open_json
from utilities.file_discovery import discover_files
from core.analyzers.analyzer_runner import run_analyzers
from core.ir_system.ir import build_project_ir
from core.ir_system.ir_writer import save_project_ir
import os


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


''''''
def generate_project_data(directory: str):

    project_name = os.path.basename(directory)
    project_dir = f"data/{project_name}"
    if os.path.exists(project_dir):
        return {"results": "Project Exist."}
    
    _initialize_project_directory(project_dir)
    file_types, total_files = discover_project_files(directory)
    analyzer_outputs = run_analysis_pipeline(file_types)
    ir = build_project_ir(analyzer_outputs)

    metadata = {
        "project_name": project_name,
        "total_files": total_files,
        "root": directory,
        "file_types": file_types,
    }

    save_project_ir(project_dir, project_name, ir, metadata)
    return metadata


def discover_project_files(directory: str):
    return discover_files(directory)


def _initialize_project_directory(project_dir: str):
    os.makedirs(project_dir, exist_ok=True)


def run_analysis_pipeline(file_types):
    analyzer_outputs = run_analyzers(file_types)
    return analyzer_outputs
