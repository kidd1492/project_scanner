# domain/analysis/project_service.py
from infrastructure.cache_system.typed_ir_cache import TypedIRCache
from utilities.file_discovery import discover_files
cache = TypedIRCache()

class ProjectService:
    def __init__(self, analyzer_manager):
        self.analyzer_manager = analyzer_manager


    def scan_project(self, root: str):

        # 1. Persistence: discover file paths
        '''this should be a class and this service should own it
        and use comp'''
        file_list = discover_files(root)

        # 2. Factory #1: file_list, root → IR objects
        '''should return the final ProjectIR'''
        project_ir = self.analyzer_manager.run_analyzers(file_list, root)
        cache.save(project_ir)

        return project_ir
