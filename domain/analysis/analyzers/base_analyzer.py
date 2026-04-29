# domain/analysis/analyzers/base_analyzer.py

from abc import ABC, abstractmethod
from typing import Any


class BaseAnalyzer(ABC):
    """
    Base class for all analyzers.

    Each analyzer:
      - declares a file_type (e.g. "py", "js", "html")
      - implements analyze_file(path, content)
      - returns IR objects (IRFile or lower-level IR nodes)
    """

    file_type: str | None = None

    @abstractmethod
    def analyze_file(self, path: str, content: str) -> Any:
        """
        Analyze a single file.

        Parameters:
            path:    file path (metadata)
            content: already-opened file text

        Returns:
            IR object (IRFile or list of IR nodes)
        """
        raise NotImplementedError("Analyzer must implement analyze_file(path, content)")
