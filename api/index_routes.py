from flask import Blueprint, request, jsonify, render_template

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    projects = index_bp.project_service.get_existing_projects()
    return render_template("index.html", projects=projects)

@index_bp.route("/dashboard/<project_name>")
def dashboard_page(project_name):
    return render_template("dashboard.html", project_name=project_name)

# API: Scan a project
@index_bp.route("/api/scan", methods=["POST"])
def api_scan_project():
    data = request.get_json()
    result = index_bp.project_service.scan_project(data)
    return jsonify(result)

# API: Get raw IR
@index_bp.route("/api/project/<project_name>")
def api_get_project(project_name):
    result = index_bp.project_service.get_project(project_name)
    return jsonify(result)

# API: List projects
@index_bp.route("/api/projects")
def api_list_projects():
    result = index_bp.project_service.get_existing_projects()
    return jsonify({"projects": result})

# API: DashboardIR
@index_bp.route("/api/dashboard/<project_name>")
def api_dashboard(project_name):
    result = index_bp.project_service.get_dashboard(project_name)
    return jsonify(result)
