# core/analyzers/base_analyzer.py

from abc import ABC, abstractmethod
from typing import Iterable, List, Any


class BaseAnalyzer(ABC):
    """
    Minimal base class for analyzers.

    Each analyzer:
      - declares a `file_type` (e.g. "py", "js", "html")
      - implements `analyze_file(path) -> IRFile`
      - inherits `analyze_files()` for batch processing
    """

    file_type: str | None = None

    @abstractmethod
    def analyze_file(self, file: str) -> Any:
        """Analyze a single file path and return an IRFile."""
        raise NotImplementedError("Analyzer must implement analyze_file()")

    def analyze_files(self, file_list: Iterable[str]) -> List[Any]:
        """Analyze a list of file paths and return a list of IRFile objects."""
        return [self.analyze_file(f) for f in file_list]
