# api/project_routes.py
from flask import Blueprint, render_template, jsonify
from analyzers.project_analyzer import analyze_project
from analyzers.base_analyzer import generate_json_reports
import os
import json

project_bp = Blueprint("project", __name__)

PROJECT_JSON = "data/project.json"


@project_bp.route("/")
def index():
    """Load the main UI page."""
    return render_template("index.html")


@project_bp.route("/project/load")
def load_project():
    """Load project.json if it exists."""
    if os.path.exists(PROJECT_JSON):
        with open(PROJECT_JSON, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"exists": False})


@project_bp.route("/project/<path:term>")
def scan_project(term):
    """Scan a new project and save project.json."""
    analyze_project(term)  # builds and saves JSON
    generate_json_reports(term)
    with open(PROJECT_JSON, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@project_bp.route("/project/files/<file_type>")
def load_files(file_type):
    """Return only the files for a specific file type."""
    if not os.path.exists(PROJECT_JSON):
        return jsonify({"exists": False})

    with open(PROJECT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for ft in data["file_types"]:
        if ft["type"] == file_type:
            return jsonify({"exists": True, "files": ft["files"]})

    return jsonify({"exists": True, "files": []})
