from flask import Blueprint, render_template, jsonify, request
from utilities.file_handling import open_json
from services.trace_service import get_trace
from test import trace_to_mermaid


trace_bp = Blueprint('trace', __name__, url_prefix='/trace')

@trace_bp.route("/traces")
def traces():
    last_data = open_json("data/last_project.json")
    last = last_data.get("last")
    return render_template("traces.html", project=last)


@trace_bp.route("/run")
def run_trace():
    last = request.args.get("project")
    trigger = request.args.get("trigger")
    trace = get_trace(last, trigger)
    return jsonify(trace)




