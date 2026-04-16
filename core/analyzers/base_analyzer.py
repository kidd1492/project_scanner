# core/analyzers/base_analyzer.py

class BaseAnalyzer:
    """
    Minimal base class for analyzers.
    """
    file_type = None

    def analyze_files(self, file_list):
        raise NotImplementedError("Analyzer must implement analyze_files()")
