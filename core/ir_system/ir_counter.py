# core/ir_system/ir_counter.py

def compute_ir_counts(project_ir):
    """
    Thin wrapper around ProjectIR.summary().
    Returns a fully typed, consistent summary dict.
    """
    return project_ir.summary()
