# core/analyzers/python_analyzer.py

import ast
from .helpers import attach_parents
from .route_extractor import RouteExtractor
from .class_extractor import ClassExtractor
from .function_extractor import FunctionExtractor
from .import_extractor import ImportExtractor
from .base_analyzer import BaseAnalyzer

class PythonAnalyzer(BaseAnalyzer):
    file_type = "py"

    def analyze_files(self, file_list):
        results = {
            "routes": [],
            "classes": [],
            "functions": [],
            "imports": []
        }

        for file in file_list:
            file = file.replace("\\", "/")
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            attach_parents(tree)

            # Imports
            imp_ex = ImportExtractor(file)
            imp_ex.visit(tree)
            results["imports"].extend(imp_ex.imports)

            # Routes
            route_ex = RouteExtractor(file)
            route_ex.visit(tree)
            results["routes"].extend(route_ex.routes)

            # Classes
            class_ex = ClassExtractor(file)
            class_ex.visit(tree)
            results["classes"].extend(class_ex.classes)

            # Functions
            func_ex = FunctionExtractor(file)
            func_ex.visit(tree)
            results["functions"].extend(func_ex.functions)

        return results
