from flask import Blueprint, render_template, jsonify
from utilities.file_handling import save_json, open_json
import os


trace_bp = Blueprint('trace', __name__, url_prefix='/trace')

DATA_DIR = "data"


# -----------------------------------------
# DASHBOARD FOR SPECIFIC PROJECT
# -----------------------------------------
@trace_bp.route("/traces")
def traces():
    last_data =  open_json("data/last_project.json")
    last = last_data.get("last")
    print(last)
    return render_template("traces.html", project=last)


