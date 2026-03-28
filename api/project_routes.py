# api/project_routes.py
from flask import Blueprint, render_template, jsonify
from services.project_info_services import get_project_info
from analyzers.base_analyzer import generate_json_reports
import os
import json

project_bp = Blueprint("project", __name__)

PROJECT_JSON = "data/project.json"
DATA_DIR = "data"



@project_bp.route("/")
def index():
    if os.path.exists(PROJECT_JSON):
        with open(PROJECT_JSON, "r", encoding="utf-8") as f:
            project = json.load(f)
        return render_template("dashboard.html", project=project)

    return render_template("dashboard_empty.html")


@project_bp.route("/project/load") 
def load_project():
    if os.path.exists(PROJECT_JSON):
        with open(PROJECT_JSON, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"exists": False})


@project_bp.route("/project/<path:term>")
def scan_project(term):
    get_project_info(term)
    generate_json_reports(term)

    with open(PROJECT_JSON, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@project_bp.route("/project/files/<file_type>")
def load_files(file_type):
    if not os.path.exists(PROJECT_JSON):
        return jsonify({"exists": False})

    with open(PROJECT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for ft in data["file_types"]:
        if ft["type"] == file_type:
            return jsonify({"exists": True, "files": ft["files"]})

    return jsonify({"exists": True, "files": []})


@project_bp.route("/analysis/<analysis_type>")
def load_analysis(analysis_type):
    path = os.path.join(DATA_DIR, f"{analysis_type}.json")

    if not os.path.exists(path):
        return jsonify({"error": "Not found"}), 404

    with open(path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))
