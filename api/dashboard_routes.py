# api/dashboard_routes.py
from flask import Blueprint, render_template, jsonify, redirect
from utilities.file_handling import save_json, open_json
import os

dashboard_bp = Blueprint("dashboard", __name__)
DATA_DIR = "data"


# -----------------------------------------
# DASHBOARD FOR SPECIFIC PROJECT
# -----------------------------------------
@dashboard_bp.route("/dashboard/<project_name>")
def dashboard(project_name):
    project_dir = os.path.join(DATA_DIR, project_name)
    project_file = os.path.join(project_dir, f"{project_name}.json")

    if not os.path.exists(project_file):
        return f"Project '{project_name}' not found.", 404

    project_data = open_json(project_file)
    save_json({"last": project_name}, "data/last_project.json")
    return render_template("dashboard.html", project=project_data)


# -----------------------------------------
# LOAD ANALYSIS JSON FILES
# -----------------------------------------
@dashboard_bp.route("/analysis/<project_name>/<analysis_type>")
def load_analysis(project_name, analysis_type):
    project_dir = os.path.join(DATA_DIR, project_name)
    file_path = os.path.join(project_dir, f"{analysis_type}.json")

    if not os.path.exists(file_path):
        return jsonify([])

    return jsonify(open_json(file_path))


# -----------------------------------------
# DASHBOARD REDIRECT — load last project
# -----------------------------------------
@dashboard_bp.route("/dashboard")
def dashboard_redirect():
    last_file = os.path.join(DATA_DIR, "last_project.json")

    if not os.path.exists(last_file):
        return render_template("index.html", projects=[])

    last = open_json(last_file).get("last")

    if not last:
        return render_template("index.html", projects=[])

    return redirect(f"/dashboard/{last}")
