# core/analyzers/base_analyzer.py

class BaseAnalyzer:
    """
    Minimal base class for analyzers.
    NO imports. NO registry. NO circular dependencies.
    """
    file_type = None

    def analyze_files(self, file_list):
        raise NotImplementedError("Analyzer must implement analyze_files()")
