# services/ingestion_service.py

from utilities.file_discovery import discover_files
from utilities.file_handling import save_json


def discover_project_files(directory: str):
    """
    Returns (file_types, total_files) for a given project root.
    """
    return discover_files(directory)


def save_project_metadata(
    project_name: str,
    root_dir: str,
    file_types,
    total_files: int,
    analysis_counts: dict
):
    """
    Persists the project metadata JSON and updates last_project.json.
    """
    project_dir = f"data/{project_name}"
    metadata = {
        "project_name": project_name,
        "total_files": total_files,
        "root": root_dir,
        "file_types": file_types,
        "analysis_counts": analysis_counts,
    }

    save_json(metadata, f"{project_dir}/{project_name}.json")
    save_json({"last": project_name}, "data/last_project.json")

    return metadata

