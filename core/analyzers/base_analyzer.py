# core/analyzers/base_analyzer.py

class BaseAnalyzer:
    """
    Base class for all analyzers.
    Each analyzer must implement analyze_files(file_list) and return a list of structured items.
    """
    file_type = None

    def analyze_files(self, file_list):
        raise NotImplementedError("Analyzer must implement analyze_files()")


# ---------------------------------------------------------
# Analyzer registry (maps file extensions to analyzer classes)
# ---------------------------------------------------------

from core.analyzers.python_analyzer import PythonAnalyzer
from core.analyzers.js_analyzer import JSAnalyzer
from core.analyzers.html_analyzer import HTMLAnalyzer

file_type_analyzer_map = {
    "py": PythonAnalyzer(),
    "js": JSAnalyzer(),
    "html": HTMLAnalyzer()
}
