from core.trace import trace_builder, trace_mermaid, trace_resolver

class TraceService:
    def __init__(self, ir_cache):
        self.ir_cache = ir_cache

    def get_triggers(self, project_name):
        ir = self.ir_cache.get(project_name)["ir"]
        files = ir["files"]

        js = []
        html = []
        api = []
        python = []

        for f in files:
            js.extend(fn["name"] for fn in f.get("js_functions", []) if fn.get("name"))
            html.extend(ev["name"] for ev in f.get("html_events", []) if ev.get("name"))
            api.extend(r["name"] for r in f.get("routes", []) if r.get("name"))
            python.extend(fn["name"] for fn in f.get("functions", []) if fn.get("name"))

        return {
            "js": sorted(set(js)),
            "html": sorted(set(html)),
            "api": sorted(set(api)),
            "python": sorted(set(python)),
        }

    def run_trace(self, project_name, trigger_name):
        ir = self.ir_cache.get(project_name)
        raw_tree = trace_resolver.resolve(ir, project_name, trigger_name)
        return trace_builder.build(raw_tree)

    def get_mermaid(self, project_name, trigger_name, diagram_type):
        ir = self.ir_cache.get(project_name)
        raw_tree = trace_resolver.resolve(ir, project_name, trigger_name)
        structured = trace_builder.build(raw_tree)
        return trace_mermaid.to_mermaid(structured, diagram_type)
