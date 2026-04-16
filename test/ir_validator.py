from utilities.file_handling import open_json

def validate_project_ir(ir):
    required_top = ["project_name", "total_files", "root", "file_types", "files"]
    for key in required_top:
        if key not in ir:
            print(f"[IR ERROR] Missing top-level key: {key}")
            return False
        print(f"[IR OK] Top-level key: {key}")

    for f in ir["files"]:
        if "path" not in f or "type" not in f:
            print(f"[IR ERROR] File missing required keys: {f.get('path')}")
            return False

        # Ensure lists exist
        for list_key in ["routes", "functions", "classes", "imports",
                         "html_events", "js_functions", "api_calls"]:
            if list_key not in f:
                print(f"[IR ERROR] Missing list '{list_key}' in file: {f['path']}")
                return False

    print("[IR OK] Structure validated.")
    return True


if __name__ == "__main__":
    project_name = "C:/Users/chris/Desktop/project_scanner/data/project_scanner/project_scanner.json"
    ir = open_json(project_name)
    #print(ir)
    validate_project_ir(ir)