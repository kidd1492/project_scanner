from flask import Blueprint, render_template, jsonify, request
from services import trace_service


trace_bp = Blueprint('trace', __name__, url_prefix='/trace')


@trace_bp.route("/<project>")
def trace_page(project):
    """
    Render the Trace Explorer UI.
    """
    return render_template("trace.html", project={"project_name": project})


@trace_bp.route("/<project>/triggers")
def list_triggers(project):
    """
    Return all possible trace triggers:
    - JS functions
    - HTML events
    - API routes
    """
    triggers = trace_service.get_triggers(project)
    return jsonify(triggers)


@trace_bp.route("/<project>/run")
def run_trace(project):
    """
    Run the trace engine for a given trigger.
    Returns the raw trace tree.
    """
    trigger = request.args.get("trigger")
    trace_tree = trace_service.run_trace(project, trigger)
    return jsonify(trace_tree)


@trace_bp.route("/<project>/mermaid")
def mermaid(project):
    """
    Convert a trace tree into a Mermaid diagram.
    """
    trigger = request.args.get("trigger")
    diagram_type = request.args.get("type", "sequence")
    mermaid_text = trace_service.get_mermaid(project, trigger, diagram_type)
    return jsonify({"mermaid": mermaid_text})




