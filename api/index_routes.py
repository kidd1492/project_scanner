# api/index_routes.py
from flask import Blueprint, render_template, jsonify
from services.project_ingestion_service import ingest_project, get_existing_projects
import os

index_bp = Blueprint("index", __name__)
DATA_DIR = "data"


# -----------------------------
# INDEX — List all project dirs
# -----------------------------
@index_bp.route("/")
def index():
    projects = get_existing_projects()
    return render_template("index.html", projects=projects)


# ---------------------------------------------------------
# LOAD PROJECT LIST
# ---------------------------------------------------------
@index_bp.route("/project/load")
def load_project():
    projects = get_existing_projects()
    return jsonify({"results": projects})


# -----------------------------------------
# SCAN PROJECT — dynamic route
# -----------------------------------------
@index_bp.route("/project/<path:term>")
def scan_project(term):
    data = ingest_project(term)
    return jsonify(data)
