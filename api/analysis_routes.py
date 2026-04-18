# api/dashboard_routes.py

from flask import Blueprint, render_template, jsonify

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analysis/<project_name>")
def analysis(project_name):
    project_data = analysis_bp.project_service.load_project(project_name)
    return render_template("analysis.html", project=project_data)