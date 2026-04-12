from utilities.file_handling import open_json
from core.trace import trace_resolver, trace_builder, trace_mermaid

def load_ir(project_name):
    """Load IR JSON from disk."""
    return open_json(f"ir/{project_name}.json")


def get_triggers(project_name):
    """Return all possible triggers from IR."""
    ir = load_ir(project_name)
    return {
        "js": ir.get("js_functions", []),
        "html": ir.get("html_events", []),
        "api": ir.get("routes", []),
        "python": ir.get("functions", [])
    }


def run_trace(project_name, trigger_name):
    """Run resolver + builder."""
    ir = load_ir(project_name)
    raw_tree = trace_resolver.resolve(ir, trigger_name)
    structured = trace_builder.build(raw_tree)
    return structured


def get_mermaid(project_name, trigger_name, diagram_type):
    """Return Mermaid diagram."""
    ir = load_ir(project_name)
    raw_tree = trace_resolver.resolve(ir, trigger_name)
    structured = trace_builder.build(raw_tree)
    return trace_mermaid.to_mermaid(structured, diagram_type)
