from domain.analysis.analyzer_manager import AnalyzerManager
from domain.analysis.analyzers.base_analyzer import BaseAnalyzer  
from utilities.file_discovery import discover_files
from utilities.file_handling import OpenFileTool


if __name__ == "__main__":

    open_file_tool = OpenFileTool()
    directory_path = "C:/Users/chris/Desktop/project_scanner"
    files = discover_files(directory_path)
    analyzer_manager = AnalyzerManager([BaseAnalyzer], open_file_tool)

    object = analyzer_manager.analyze_files(files)
    print(object[0])


