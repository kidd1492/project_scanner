# api/dashboard_routes.py

from flask import Blueprint, render_template, jsonify, redirect
from services.project_service import load_project
from services.dashboard_service import (
    get_counts,
    generate_charts,
    load_last_dashboard
)

dashboard_bp = Blueprint("dashboard", __name__)


# Dashboard for a specific project
@dashboard_bp.route("/dashboard/<project_name>")
def dashboard(project_name):
    project_data = load_project(project_name)
    return render_template("dashboard.html", project=project_data)


# Return IR-based counts for overview panel
@dashboard_bp.route("/dashboard/<project_name>/counts")
def dashboard_counts(project_name):
    return jsonify(get_counts(project_name))


# Generate all charts for dashboard
@dashboard_bp.route("/dashboard/<project_name>/charts")
def dashboard_charts(project_name):
    return jsonify(generate_charts(project_name))


# Redirect to last opened project
@dashboard_bp.route("/dashboard")
def dashboard_redirect():
    last = load_last_dashboard()
    if last == "no_file":
        return render_template("index.html", projects=[])
    return redirect(f"/dashboard/{last}")
