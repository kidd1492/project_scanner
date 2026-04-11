# api/index_routes.py
from flask import Blueprint, render_template, jsonify
from services.project_service import get_existing_projects, generate_project_data

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
    result = generate_project_data(term)
    return jsonify(result)