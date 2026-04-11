# services/dashboard_service.py

import os
from utilities.file_handling import open_json

from core.ir_system.ir_reader import load_ir
from core.ir_system.ir_counter import compute_ir_counts
from core.chart_system.chart_generator import generate_all_charts

DATA_DIR = "data"


# ---------------------------------------------------------
# 1. Return IR-based counts for the overview panel
# ---------------------------------------------------------
def get_counts(project_name):
    ir = load_ir(project_name)
    return compute_ir_counts(ir)


# ---------------------------------------------------------
# 2. Generate all dashboard charts (5 PNGs)
# ---------------------------------------------------------
def generate_charts(project_name):
    ir = load_ir(project_name)
    generate_all_charts(ir, project_name)
    return {"status": "ok"}


# ---------------------------------------------------------
# 3. Load last opened project
# ---------------------------------------------------------
def load_last_dashboard():
    last_file = os.path.join(DATA_DIR, "last_project.json")
    if not os.path.exists(last_file):
        return "no_file"

    last = open_json(last_file).get("last")
    if not last:
        return "no_file"

    return last
