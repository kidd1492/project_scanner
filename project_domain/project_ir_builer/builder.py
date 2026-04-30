# project_domain/project_ir_builder/project_ir_builder.py

import os
from project_domain.project_ir import ProjectIR

class ProjectIRBuilder:
    """Pure, deterministic builder for ProjectIR."""

    def build(self, directory: str, ir_files: list) -> ProjectIR:
        return ProjectIR(
            project_name=os.path.basename(directory),
            total_files=len(ir_files),
            root=directory,
            files=ir_files,
        )
