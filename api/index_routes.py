# api/index_routes.py
from flask import Blueprint, render_template, jsonify
from services.project_orchestrator import scan_project_files, get_existing_projects


index_bp = Blueprint("index", __name__)
DATA_DIR = "data"


# -----------------------------
# INDEX — List all project dirs
# -----------------------------
@index_bp.route("/")
def index():
    projects = get_existing_projects()
    return render_template("index.html", projects=projects)


@index_bp.route("/project/<path:term>")
def scan_project(term):
    result = scan_project_files(term)
    return jsonify(result)