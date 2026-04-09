import os, json


def save_analyzer_results(results, type, output_dir):
    # Special handling for Python: split into 3 JSON files
    if type == "py":
        save_python_outputs(results, output_dir)
    elif type != "py":
        output_path = os.path.join(output_dir, f"{type}.json")
        save_json(results, output_path)
        

def save_python_outputs(results, output_dir):
    """Save API, classes, and functions as separate JSON files."""
    api_path = os.path.join(output_dir, "api.json")
    classes_path = os.path.join(output_dir, "classes.json")
    functions_path = os.path.join(output_dir, "functions.json")

    save_json(results["routes"], api_path)
    save_json(results["classes"], classes_path)
    save_json(results["functions"], functions_path)


def save_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return


def open_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        return content
    

def embed_ir_into_project_json(project_dir, project_name, ir):
    project_json_path = os.path.join(project_dir, f"{project_name}.json")

    with open(project_json_path, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    project_data["ir"] = ir

    with open(project_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=4)

