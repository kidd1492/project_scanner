# api/trace_routes.py

from flask import Blueprint, render_template, jsonify, request

trace_bp = Blueprint("trace", __name__, url_prefix="/trace")

@trace_bp.route("/<project>")
def trace_page(project):
    return render_template("trace.html", project={"project_name": project})

@trace_bp.route("/<project>/triggers")
def list_triggers(project):
    triggers = trace_bp.trace_service.get_triggers(project)
    return jsonify(triggers)

@trace_bp.route("/<project>/run")
def run_trace(project):
    trigger = request.args.get("trigger")
    trace_tree = trace_bp.trace_service.run_trace(project, trigger)
    return jsonify(trace_tree)

@trace_bp.route("/<project>/mermaid")
def mermaid(project):
    trigger = request.args.get("trigger")
    diagram_type = request.args.get("type", "sequence")
    mermaid_text = trace_bp.trace_service.get_mermaid(project, trigger, diagram_type)
    return jsonify({"mermaid": mermaid_text})
