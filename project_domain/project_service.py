# domain/analysis/project_service.py

from utilities.file_discovery import discover_files
from project_domain.builder import build_project_ir

class ProjectService:
    def __init__(self, analyzer_manager, builder):
        self.analyzer_manager = analyzer_manager
        self.builder = builder

    def scan_project(self, root: str):
        # 1. Persistence: discover file paths
        file_list = discover_files(root)

        # 2. Factory #1: analyzers → IR objects
        ir_objects = self.analyzer_manager.run_analyzers(file_list)

        # 3. Factory #2: IR objects → IRFile
        # ir_files = self.builder.build_files(ir_objects)

        # 4. Factory #3: IRFile → ProjectIR
        return build_project_ir(root, ir_objects)

        #return ir_objects
