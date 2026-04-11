# services/explorer_service.py

from core.ir_system.ir_reader import (
    load_ir,
    list_files,
    get_file,
    get_symbol_by_id
)


# ---------------------------------------------------------
# Return list of all files in the IR
# ---------------------------------------------------------
def list_project_files(project_name):
    ir = load_ir(project_name)
    return list_files(ir)


# ---------------------------------------------------------
# Return details for a specific file
# ---------------------------------------------------------
def get_file_details(project_name, path):
    ir = load_ir(project_name)
    return get_file(ir, path)


# ---------------------------------------------------------
# Return details for a specific symbol
# ---------------------------------------------------------
def get_symbol_details(project_name, symbol_id):
    ir = load_ir(project_name)
    return get_symbol_by_id(ir, symbol_id)
