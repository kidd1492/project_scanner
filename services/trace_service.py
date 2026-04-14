from utilities.file_handling import load_ir
from core.trace import trace_resolver, trace_builder, trace_mermaid


def get_triggers(project_name):
    """Return all possible triggers from IR."""
    ir = load_ir(project_name)
    files = ir["ir"]["files"]

    js = []
    html = []
    api = []
    python = []

    for f in files:
        for fn in f.get("js_functions", []):
            name = fn.get("name")
            if name:
                js.append(name)

        for ev in f.get("html_events", []):
            name = ev.get("name")
            if name:
                html.append(name)

        for r in f.get("routes", []):
            name = r.get("name")
            if name:
                api.append(name)

        for fn in f.get("functions", []):
            name = fn.get("name")
            if name:
                python.append(name)

    return {
        "js": sorted(set(js)),
        "html": sorted(set(html)),
        "api": sorted(set(api)),
        "python": sorted(set(python)),
    }


def run_trace(project_name, trigger_name):
    """Run resolver + builder."""
    ir = load_ir(project_name)
    raw_tree = trace_resolver.resolve(ir, project_name, trigger_name)
    structured = trace_builder.build(raw_tree)
    return structured


def get_mermaid(project_name, trigger_name, diagram_type):
    """Return Mermaid diagram."""
    ir = load_ir(project_name)
    raw_tree = trace_resolver.resolve(ir, project_name, trigger_name)
    structured = trace_builder.build(raw_tree)
    return trace_mermaid.to_mermaid(structured, diagram_type)
