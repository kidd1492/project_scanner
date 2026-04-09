# api/dashboard_routes.py
from flask import Blueprint, render_template, jsonify, redirect
from services.project_service import load_project, load_analysis_type, load_last_dashboard
import os
from pathlib import Path

dashboard_bp = Blueprint("dashboard", __name__)
DATA_DIR = "data"

# DASHBOARD FOR SPECIFIC PROJECT
@dashboard_bp.route("/dashboard/<project_name>")
def dashboard(project_name):
    project_data = load_project(project_name)
    return render_template("dashboard.html", project=project_data)


# LOAD ANALYSIS JSON FILES
@dashboard_bp.route("/analysis/<project_name>/<analysis_type>")
def load_analysis(project_name, analysis_type):
    results = load_analysis_type(project_name, analysis_type)
    return jsonify(results)


# DASHBOARD REDIRECT — load last project
@dashboard_bp.route("/dashboard")
def dashboard_redirect():
    last = load_last_dashboard()
    if last == "no_file":
        return render_template("index.html", projects=[])
    
    return redirect(f"/dashboard/{last}")


@dashboard_bp.route("/files/<project>/<ftype>")
def get_files(project, ftype):
    project_data = load_project(project)  # however you load it

    # Find the matching file type entry
    for ft in project_data["file_types"]:
        if ft["type"] == ftype:
            return jsonify({"type": ftype, "files": ft["files"]})

    return jsonify({"type": ftype, "files": []})



@dashboard_bp.route("/file/<path:filename>")
def get_file(filename):
    print("RAW:", filename)

    # Convert POSIX path back to OS path
    filepath = Path(filename)

    if not filepath.exists():
        return jsonify({"error": "File not found"}), 404

    content = filepath.read_text(encoding="utf-8", errors="ignore")

    return jsonify({
        "filename": filename,
        "content": content
    })


@dashboard_bp.route("/fileinfo/<project>/<path:filename>")
def get_file_info(project, filename):
    project_data = load_project(project)
    ir_files = project_data.get("ir", {}).get("files", [])

    # Normalize path
    filename = filename.replace("\\", "/")

    # Find matching IR entry
    for f in ir_files:
        if f["path"] == filename:
            return jsonify(f)

    return jsonify({"error": "File not found in IR"}), 404
