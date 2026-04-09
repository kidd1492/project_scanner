# api/dashboard_routes.py
from flask import Blueprint, render_template, jsonify, redirect
from services.project_service import load_project, load_analysis_type, load_last_dashboard
import os

dashboard_bp = Blueprint("dashboard", __name__)
DATA_DIR = "data"

# DASHBOARD FOR SPECIFIC PROJECT
@dashboard_bp.route("/dashboard/<project_name>")
def dashboard(project_name):
    project_data = load_project(project_name)
    return render_template("dashboard.html", project=project_data)


# LOAD ANALYSIS JSON FILES
@dashboard_bp.route("/analysis/<project_name>/<analysis_type>")
def load_analysis(project_name, analysis_type):
    results = load_analysis_type(project_name, analysis_type)
    return jsonify(results)


# DASHBOARD REDIRECT — load last project
@dashboard_bp.route("/dashboard")
def dashboard_redirect():
    last = load_last_dashboard()
    if last == "no_file":
        return render_template("index.html", projects=[])
    
    return redirect(f"/dashboard/{last}")
