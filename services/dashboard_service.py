# services/dashboard_service.py

from core.ir_system.ir_counter import compute_ir_counts
from core.chart_system.chart_generator import generate_all_charts

class DashboardService:
    def __init__(self, typed_ir_cache):
        self.typed_ir_cache = typed_ir_cache

    def get_counts_typed(self, project_name):
        project_ir = self.typed_ir_cache.load(project_name)
        if not project_ir:
            return {"error": "IR not found", "total_files": 0}

        return compute_ir_counts(project_ir)

    def generate_charts(self, project_name):
        project_ir = self.typed_ir_cache.load(project_name)
        if not project_ir:
            return {"status": "error"}

        generate_all_charts(project_ir, project_name)
        return {"status": "ok"}
