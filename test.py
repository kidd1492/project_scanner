# test.py

from infrastructure.file_system.file_handling import FileReader
from infrastructure.file_system.file_discovery import FileDiscovery
from infrastructure.cache_system.typed_ir_cache import TypedIRCache
from project_domain.project_ir_builer.builder import ProjectIRBuilder
from project_domain.project_ir_builer.analyzer_manager import AnalyzerManager
from project_domain.project_service import ProjectService


if __name__ == "__main__":
    directory_path = "C:/Users/chris/Desktop/project_scanner_refactor"

    # --- Infrastructure Tools ---
    file_discovery = FileDiscovery()
    file_reader = FileReader()
    persistence = TypedIRCache(cache_dir="cache", file_reader=file_reader)

    # --- Builder Layer ---
    project_ir_builder = ProjectIRBuilder()
    analyzer_manager = AnalyzerManager(
        open_file_tool=file_reader,
        project_ir_builder=project_ir_builder
    )

    # --- Service Layer ---
    project_service = ProjectService(
        discover_files=file_discovery,
        analyzer_manager=analyzer_manager,
        persistance=persistence
    )

    # --- Execute Scan ---
    project_ir = project_service.scan_project(directory_path)

    print("Total files:", project_ir.total_files)
    print("Project name:", project_ir.project_name)
    print("Root:", project_ir.root)
