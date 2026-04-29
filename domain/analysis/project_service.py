from .project_ir import ProjectIR
from utilities.file_discovery import discover_files


class ProjectService:
    def __init__(self, analyzer_manager, builder):
        self.analyzer_manager = analyzer_manager
        self.builder = builder

    def scan_project(self, root: str):
        paths = discover_files(root)
        semantic_objects = self.analyzer_manager.analyze_files(paths)
        ir_files = self.builder.build_files(semantic_objects)
        return self.builder.build_project_ir(root, ir_files)

