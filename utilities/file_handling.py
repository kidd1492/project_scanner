import os, json


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