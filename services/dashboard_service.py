from core.ir_system.ir_counter import compute_ir_counts
from core.chart_system.chart_generator import generate_all_charts

class DashboardService:
    def __init__(self, ir_cache):
        self.ir_cache = ir_cache

    def get_counts(self, project_name):
        ir = self.ir_cache.get(project_name)["ir"]
        return compute_ir_counts(ir)

    def generate_charts(self, project_name):
        ir = self.ir_cache.get(project_name)["ir"]
        generate_all_charts(ir, project_name)
        return {"status": "ok"}
