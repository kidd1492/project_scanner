# domain/analysis/project_service.py

class ProjectService:
    def __init__(self, discover_files, analyzer_manager, persistance):
        self.discover_files = discover_files
        self.analyzer_manager = analyzer_manager
        self.persistance = persistance

    def scan_project(self, root: str):        
        file_list = self.discover_files(root)

        # 2. ProjectIR Factory: file_list, root → IR objects
        project_ir = self.analyzer_manager.run_analyzers(file_list, root)
        self.persistance.save(project_ir)
        return project_ir
    
    def get_existing_projects(self):
        return self.persistance.list_all_projects()
