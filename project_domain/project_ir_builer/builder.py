# core/ir_system/builder.py

import os
from project_domain.project_ir import ProjectIR


def build_project_ir(directory, ir_files: list) -> ProjectIR:
    
    ir_files = ir_files

    return ProjectIR(
        project_name=os.path.basename(directory),
        total_files=len(ir_files),
        root=directory,
        files=ir_files,
    )
