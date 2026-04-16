# services/dashboard_service.py

from core.ir_system.ir_counter import compute_ir_counts
from core.chart_system.chart_generator import generate_all_charts

class DashboardService:
    def __init__(self, ir_cache):
        self.ir_cache = ir_cache

    def get_counts(self, project_name):
        project_ir = self.ir_cache.load(project_name)

        if not project_ir:
            return {"error": "IR not found", "total_files": 0}

        # Ensure correct shape
        if "files" not in project_ir:
            print("ERROR: IR missing 'files' key")
            return {"error": "Invalid IR format", "total_files": 0}

        return compute_ir_counts(project_ir)

    def generate_charts(self, project_name):
        project_ir = self.ir_cache.load(project_name)

        print("DEBUG: Loaded IR for charts:", type(project_ir), project_ir)

        if not project_ir or "files" not in project_ir:
            print("ERROR: Cannot generate charts, IR invalid")
            return {"status": "error"}

        generate_all_charts(project_ir, project_name)
        return {"status": "ok"}
