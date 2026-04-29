from domain.analysis.analyzer_manager import AnalyzerManager
from domain.analysis.project_service import ProjectService
from domain.analysis import builder
from domain.analysis.analyzers.base_analyzer import BaseAnalyzer
from infrastructure.file_system.file_handling import OpenFileTool

if __name__ == "__main__":

    directory_path = "C:/Users/chris/Desktop/project_scanner"
    base_analyzer = BaseAnalyzer
    analyzer_manager = AnalyzerManager(base_analyzer, open_file_tool=OpenFileTool())
    project_service = ProjectService(analyzer_manager, builder)
    analyzed = project_service.scan_project(directory_path)
    print(analyzed)


