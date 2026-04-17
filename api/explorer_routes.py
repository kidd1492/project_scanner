# api/explorer_routes.py

from flask import Blueprint, jsonify, render_template

explorer_bp = Blueprint("explorer", __name__)

@explorer_bp.route("/explorer/<project_name>")
def explorer_page(project_name):
    project_data = explorer_bp.project_service.load_project(project_name)
    return render_template("explorer.html", project=project_data)

@explorer_bp.route("/explorer/<project_name>/files")
def explorer_files(project_name):
    return jsonify(explorer_bp.explorer_service.list_project_files(project_name))

@explorer_bp.route("/explorer/<project_name>/file/<path:filepath>")
def explorer_file_details(project_name, filepath):
    details = explorer_bp.explorer_service.get_file_details(project_name, filepath)
    if details is None:
        return jsonify({"error": "File not found"}), 404
    return jsonify(details)

@explorer_bp.route("/explorer/<project_name>/symbol/<path:symbol_id>")
def explorer_symbol_details(project_name, symbol_id):
    details = explorer_bp.explorer_service.get_symbol_details(project_name, symbol_id)
    if details is None:
        return jsonify({"error": "Symbol not found"}), 404
    return jsonify(details)

@explorer_bp.route("/explorer/<project_name>/source/<path:filepath>")
def explorer_file_source(project_name, filepath):
    full = explorer_bp.explorer_service.get_file_source(filepath)
    return jsonify({"source": full})
