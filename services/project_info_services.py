from analyzers.helpers import analyze_project, save_json


def get_project_info(directory:str):
    data = analyze_project(directory)
    save_json(data, "data/project.json")
    print(data)