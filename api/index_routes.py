# api/index_routes.py

from flask import Blueprint, request, jsonify, render_template

index_bp = Blueprint("index", __name__)


# -----------------------------
# Landing Page (HTML)
# -----------------------------
@index_bp.route("/")
def landing_page():
    return render_template("index.html")


# -----------------------------
# Dashboard Page (HTML)
# -----------------------------
@index_bp.route("/dashboard/<project_name>")
def dashboard_page(project_name):
    return render_template("dashboard.html", project_name=project_name)


# -----------------------------
# API: Scan a project
# -----------------------------
@index_bp.route("/api/scan", methods=["POST"])
def api_scan_project():
    data = request.get_json()
    path = data.get("path")

    if not path:
        return jsonify({"error": "No path provided"}), 400

    try:
        project_ir = index_bp.project_service.scan_project(path)
        return jsonify(project_ir.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# API: Get a scanned project (raw IR)
# -----------------------------
@index_bp.route("/api/project/<project_name>")
def api_get_project(project_name):
    project_ir = index_bp.project_service.persistance.load(project_name)

    if not project_ir:
        return jsonify({"error": "Project not found"}), 404

    return jsonify(project_ir.to_dict())


# -----------------------------
# API: List all scanned projects
# -----------------------------
@index_bp.route("/api/projects")
def api_list_projects():
    cache = index_bp.project_service.persistance._cache
    return jsonify({"projects": list(cache.keys())})


# -----------------------------
# API: Dashboard Data (DashboardIR)
# -----------------------------
@index_bp.route("/api/dashboard/<project_name>")
def api_dashboard(project_name):
    project_ir = index_bp.project_service.persistance.load(project_name)

    if not project_ir:
        return jsonify({"error": "Project not found"}), 404

    dashboard_ir = index_bp.dashboard_builder.build(project_ir)
    return jsonify(dashboard_ir.to_dict())
