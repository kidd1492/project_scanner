# domain/analysis/project_service.py

class ProjectService:
    def __init__(self, discover_files, analyzer_manager, persistance):
        self.discover_files = discover_files
        self.analyzer_manager = analyzer_manager
        self.persistance = persistance

    def scan_project(self, root: str):

        # 1. Persistence: discover file paths
        '''this should be a class and this service should own it
        and use comp'''
        file_list = self.discover_files(root)

        # 2. Factory #1: file_list, root → IR objects
        '''should return the final ProjectIR'''
        project_ir = self.analyzer_manager.run_analyzers(file_list, root)
        self.persistance.save(project_ir)

        return project_ir
