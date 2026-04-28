from .analyzers.base_analyzer import BaseAnalyzer

class AnalyzerManager:
    def __init__(self, analyzers: list[BaseAnalyzer], open_file_tool):
        self.analyzers = analyzers
        self.open_file_tool = open_file_tool

    def analyze_files(self, files: list[str]):
        all_objects = []
        for path in files:
            analyzer = self._pick_analyzer(path)
            if not analyzer:
                continue
            content = self.open_file_tool.read(path)
            all_objects.extend(analyzer.analyze(path, content))
        return all_objects
