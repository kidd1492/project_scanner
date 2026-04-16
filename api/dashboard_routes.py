from flask import Blueprint, render_template, jsonify

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/<project_name>")
def dashboard(project_name):
    project_data = dashboard_bp.project_service.load_project(project_name)
    return render_template("dashboard.html", project=project_data)

@dashboard_bp.route("/counts/<project_name>")
def get_counts(project_name):
    result = dashboard_bp.dashboard_service.get_counts_typed(project_name)
    return jsonify(result)

@dashboard_bp.route("/dashboard/<project_name>/charts")
def dashboard_charts(project_name):
    return jsonify(dashboard_bp.dashboard_service.generate_charts(project_name))
