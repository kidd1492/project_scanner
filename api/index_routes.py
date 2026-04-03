# api/index_routes.py
from flask import Blueprint, render_template, jsonify
from services.project_info_services import get_project_info
import os

index_bp = Blueprint("index", __name__)
DATA_DIR = "data"


# -----------------------------
# INDEX — List all project dirs
# -----------------------------
@index_bp.route("/")
def index():
    project_dirs = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                project_dirs.append(name)

    return render_template("index.html", projects=project_dirs)


# ---------------------------------------------------------
# LOAD PROJECT LIST
# ---------------------------------------------------------
@index_bp.route("/project/load")
def load_project():
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)

    return jsonify({"results": projects})


# -----------------------------------------
# SCAN PROJECT — dynamic route
# -----------------------------------------
@index_bp.route("/project/<path:term>")
def scan_project(term):
    data = get_project_info(term)
    return jsonify(data)
