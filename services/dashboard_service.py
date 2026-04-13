# services/dashboard_service.py
from services.trace_service import load_ir
#from core.ir_system.ir_reader import load_ir
from core.ir_system.ir_counter import compute_ir_counts
from core.chart_system.chart_generator import generate_all_charts

DATA_DIR = "data"

# 1. Return IR-based counts for the overview panel
def get_counts(project_name):
    ir = load_ir(project_name).get("ir", {})
    return compute_ir_counts(ir)


# 2. Generate all dashboard charts (5 PNGs)
def generate_charts(project_name):
    ir = load_ir(project_name).get("ir", {})
    generate_all_charts(ir, project_name)
    return {"status": "ok"}
