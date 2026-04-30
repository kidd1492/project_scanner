from project_domain.project_ir_builer.analyzer_manager import AnalyzerManager
from project_domain.project_service import ProjectService

from infrastructure.file_system.file_handling import OpenFileTool

if __name__ == "__main__":
    directory_path = "C:/Users/chris/Desktop/project_scanner"

    analyzer_manager = AnalyzerManager(open_file_tool=OpenFileTool())
    project_service = ProjectService(analyzer_manager)
    analyzed = project_service.scan_project(directory_path)
    print(analyzed.total_files)
