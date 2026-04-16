# services/trace_service.py

from core.trace import trace_builder, trace_mermaid, trace_resolver


class TraceService:
    def __init__(self, ir_cache):
        self.ir_cache = ir_cache

    def get_triggers(self, project_name):
        project_ir = self.ir_cache.load(project_name)

        js = []
        html = []
        api = []
        python = []

        for f in project_ir["files"]:
            js.extend(fn["name"] for fn in f.get("js_functions", []))
            html.extend(e["name"] for e in f.get("html_events", []))
            api.extend(r["name"] for r in f.get("routes", []))
            python.extend(fn["name"] for fn in f.get("functions", []))

        return {
            "js": sorted(set(js)),
            "html": sorted(set(html)),
            "api": sorted(set(api)),
            "python": sorted(set(python)),
        }

    def run_trace(self, project_name, trigger_name):
        project_ir = self.ir_cache.load(project_name)
        raw_tree = trace_resolver.resolve(project_ir, project_name, trigger_name)
        return trace_builder.build(raw_tree)

    def get_mermaid(self, project_name, trigger_name, diagram_type):
        project_ir = self.ir_cache.load(project_name)
        raw_tree = trace_resolver.resolve(project_ir, project_name, trigger_name)
        structured = trace_builder.build(raw_tree)
        return trace_mermaid.to_mermaid(structured, diagram_type)
