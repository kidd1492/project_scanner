import os, json

def save_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return


def open_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        return content

def load_ir(project_name):
    """Load IR JSON from disk."""
    return open_json(f"data/{project_name}/{project_name}.json") 