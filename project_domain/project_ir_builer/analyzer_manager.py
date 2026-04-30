# project_domain/project_ir_builder/analyzer_manager.py

#from project_domain.project_ir_builer.builder import build_project_ir
from project_domain.project_ir_builer.analyzers.python_analyzer import PythonAnalyzer
from project_domain.project_ir_builer.analyzers.html_analyzer import HTMLAnalyzer
from project_domain.project_ir_builer.analyzers.js_analyzer import JSAnalyzer


class AnalyzerManager:
    def __init__(self, open_file_tool, project_ir_builder):
        self.open_file_tool = open_file_tool
        self.project_ir_builder = project_ir_builder

        self.file_type_analyzer_map = {
            "py": PythonAnalyzer(),
            "js": JSAnalyzer(),
            "html": HTMLAnalyzer(),
        }

    def run_analyzers(self, file_list, root):
        final = []

        for path in file_list:
            ext = path.split(".")[-1]
            analyzer = self.file_type_analyzer_map.get(ext)
            if not analyzer:
                continue

            content = self.open_file_tool.read_text(path)
            ir_obj = analyzer.analyze_file(path, content)
            final.append(ir_obj)

        return self.project_ir_builder.build(root, final)
