
from project_domain.project_ir_builer_service.analyzers.python_analyzer import PythonAnalyzer
from project_domain.project_ir_builer_service.analyzers.html_analyzer import HTMLAnalyzer
from project_domain.project_ir_builer_service.analyzers.js_analyzer import JSAnalyzer


class AnalyzerManager:
    def __init__(self, open_file_tool):
        self.open_file_tool = open_file_tool

        self.file_type_analyzer_map = {
            "py": PythonAnalyzer(),
            "js": JSAnalyzer(),
            "html": HTMLAnalyzer(),
        }

    def run_analyzers(self, file_list):
        """
        file_list = ["a.py", "b.js", "c.html"]
        """

        final = []

        for path in file_list:
            ext = path.split(".")[-1]

            analyzer = self.file_type_analyzer_map.get(ext)
            if not analyzer:
                continue

            content = self.open_file_tool(path)
            ir_obj = analyzer.analyze_file(path, content)

            final.append(ir_obj)

        return final
