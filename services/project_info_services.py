from analyzers.helpers import analyze_project, save_json
from analyzers.base_analyzer import generate_json_reports


def get_project_info(directory:str):
    data = analyze_project(directory)
    save_json(data, f"data/{data['project_name']}.json")
    generate_json_reports(directory)
    return data

