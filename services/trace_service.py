# services/trace_service.py

from core.trace import trace_builder, trace_mermaid, trace_resolver

class TraceService:
    def __init__(self, typed_ir_cache):
        self.typed_ir_cache = typed_ir_cache

    def get_triggers(self, project_name):
        project_ir = self.typed_ir_cache.get(project_name)

        return {
            "js": sorted({fn.name for fn in project_ir.get_js_functions()}),
            "html": sorted({ev.name for ev in project_ir.get_html_events()}),
            "api": sorted({r.name for r in project_ir.get_routes()}),
            "python": sorted({
                fn.name for fn in project_ir.get_all_symbols()
                if hasattr(fn, "args")
            }),
        }

    def run_trace(self, project_name, trigger_name):
        project_ir = self.typed_ir_cache.get(project_name)
        raw_tree = trace_resolver.resolve(project_ir, trigger_name)
        return trace_builder.build(raw_tree)

    def get_mermaid(self, project_name, trigger_name, diagram_type):
        project_ir = self.typed_ir_cache.get(project_name)
        raw_tree = trace_resolver.resolve(project_ir, trigger_name)
        structured = trace_builder.build(raw_tree)
        return trace_mermaid.to_mermaid(structured, diagram_type)
