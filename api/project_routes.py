# api/project_routes.py
from flask import Blueprint, render_template, jsonify, redirect
from services.project_info_services import get_project_info
from analyzers.helpers import save_json, open_json
import os

project_bp = Blueprint("project", __name__)

DATA_DIR = "data"


@project_bp.route("/")
def index():
    project_dirs = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                project_dirs.append(name)

    return render_template("index.html", projects=project_dirs)


@project_bp.route("/project/load")
def load_project():
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)

    return jsonify({"results": projects})


@project_bp.route("/project/<path:term>")
def scan_project(term):
    data = get_project_info(term)
    return jsonify(data)


@project_bp.route("/dashboard/<project_name>")
def dashboard(project_name):
    project_dir = os.path.join(DATA_DIR, project_name)
    project_file = os.path.join(project_dir, f"{project_name}.json")

    if not os.path.exists(project_file):
        return f"Project '{project_name}' not found.", 404

    project_data = open_json(project_file)
    return render_template("dashboard.html", project=project_data)


@project_bp.route("/analysis/<project_name>/<analysis_type>")
def load_analysis(project_name, analysis_type):
    project_dir = os.path.join(DATA_DIR, project_name)
    file_path = os.path.join(project_dir, f"{analysis_type}.json")

    if not os.path.exists(file_path):
        return jsonify([])

    return jsonify(open_json(file_path))


# -----------------------------------------
# DASHBOARD REDIRECT — load last project
# -----------------------------------------
@project_bp.route("/dashboard")
def dashboard_redirect():
    last_file = os.path.join(DATA_DIR, "last_project.json")

    if not os.path.exists(last_file):
        return render_template("index.html", projects=[])

    last = open_json(last_file).get("last")

    if not last:
        return render_template("index.html", projects=[])

    return redirect(f"/dashboard/{last}")
