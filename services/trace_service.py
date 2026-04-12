from utilities.file_handling import open_json
from core.trace import trace_resolver, trace_builder, trace_mermaid


def load_ir(project_name):
    """Load IR JSON from disk."""
    return open_json(f"data/{project_name}/{project_name}.json")


def get_triggers(project_name):
    """Return all possible triggers from IR."""
    ir = load_ir(project_name)

    # IMPORTANT: your IR stores files under ir["ir"]["files"]
    file_list = ir.get("ir", {}).get("files", [])

    js = []
    html = []
    api = []
    python = []

    for f in file_list:
        # JS functions
        for fn in f.get("js_functions", []):
            name = fn.get("name")
            if name:
                js.append(name)

        # HTML events
        for ev in f.get("html_events", []):
            name = ev.get("name")
            if name:
                html.append(name)

        # API routes
        for r in f.get("routes", []):
            name = r.get("name")
            if name:
                api.append(name)

        # Python functions
        for fn in f.get("functions", []):
            name = fn.get("name")
            if name:
                python.append(name)

    return {
        "js": js,
        "html": html,
        "api": api,
        "python": python
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
