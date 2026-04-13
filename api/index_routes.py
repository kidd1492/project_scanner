# api/index_routes.py
from flask import Blueprint, render_template, jsonify
from services import project_service
import os


index_bp = Blueprint("index", __name__)
DATA_DIR = "data"


# -----------------------------
# INDEX — List all project dirs
# -----------------------------
@index_bp.route("/")
def index():
    projects = project_service.get_existing_projects()
    return render_template("index.html", projects=projects)


@index_bp.route("/project/<path:term>")
def scan_project(term):
    if not os.path.isdir(term):
        return jsonify({"results": "Invalid Path"}), 400
    result = project_service.generate_project_data(term)
    return jsonify(result)