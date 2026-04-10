# core/analyzers/import_extractor.py

import ast

class ImportExtractor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/")
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                "type": "import",
                "module": alias.name,
                "symbol": None,
                "alias": alias.asname,
                "file": self.file_path,
                "source": self.file_path.split("/")[-1],
                "line": node.lineno
            })

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imports.append({
                "type": "import",
                "module": module,
                "symbol": alias.name,
                "alias": alias.asname,
                "file": self.file_path,
                "source": self.file_path.split("/")[-1],
                "line": node.lineno
            })
