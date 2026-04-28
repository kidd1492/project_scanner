from .project_ir import ProjectIR



class ProjectService:
    def __init__(self, file_repo, service_manager, builder):
        self.file_repo = file_repo
        self.service_manager = service_manager
        self.builder = builder

    def scan_project(self, root: str):
        paths = self.file_repo.list_files(root)
        semantic_objects = self.service_manager.build_semantic_objects(paths)
        ir_files = self.builder.build_files(semantic_objects)
        return self.builder.build_project_ir(root, ir_files)

