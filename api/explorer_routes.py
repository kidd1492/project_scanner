# api/explorer_routes.py
from services.project_service import load_project
from flask import Blueprint, jsonify, render_template
from services.explorer_service import (
    list_project_files,
    get_file_details,
    get_symbol_details,
    get_file_source
)

explorer_bp = Blueprint("explorer", __name__)

# ---------------------------------------------------------
# PAGE ROUTE — Explorer UI
# ---------------------------------------------------------
@explorer_bp.route("/explorer/<project_name>")
def explorer_page(project_name):
    project_data = load_project(project_name)
    return render_template("explorer.html", project=project_data)



# ---------------------------------------------------------
# 1. List all files in the project
# ---------------------------------------------------------
@explorer_bp.route("/explorer/<project_name>/files")
def explorer_files(project_name):
    files = list_project_files(project_name)
    return jsonify(files)


# ---------------------------------------------------------
# 2. Get details for a specific file
# ---------------------------------------------------------
@explorer_bp.route("/explorer/<project_name>/file/<path:filepath>")
def explorer_file_details(project_name, filepath):
    details = get_file_details(project_name, filepath)
    if details is None:
        return jsonify({"error": "File not found"}), 404
    return jsonify(details)


# ---------------------------------------------------------
# 3. Get details for a specific symbol
# ---------------------------------------------------------
@explorer_bp.route("/explorer/<project_name>/symbol/<path:symbol_id>")
def explorer_symbol_details(project_name, symbol_id):
    details = get_symbol_details(project_name, symbol_id)
    if details is None:
        return jsonify({"error": "Symbol not found"}), 404
    return jsonify(details)


@explorer_bp.route("/explorer/<project_name>/source/<path:filepath>")
def explorer_file_source(project_name, filepath):
    full = get_file_source(project_name, filepath)
    return jsonify({"source": full})
