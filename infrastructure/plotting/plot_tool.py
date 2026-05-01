import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


class PlotTool:
    def __init__(self, base_dir="web_app/static/projects"):
        self.base_dir = base_dir

    # -----------------------------
    # Internal helper
    # -----------------------------
    def _ensure_output_dir(self, project_name):
        path = os.path.join(self.base_dir, project_name)
        os.makedirs(path, exist_ok=True)
        return path

    # -----------------------------
    # 1. File Type Pie Chart
    # -----------------------------
    def file_type_pie(self, project_ir, project_name):
        counts = project_ir.count_file_types()

        labels = list(counts.keys())
        sizes = list(counts.values())

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("File Type Distribution")

        out = self._ensure_output_dir(project_name)
        plt.savefig(f"{out}/file_types.png", bbox_inches='tight')
        plt.close()

    # -----------------------------
    # 2. Symbol Distribution Bar
    # -----------------------------
    def symbol_distribution(self, project_ir, project_name):
        counts = project_ir.summary()

        labels = ["Functions", "Classes", "Methods", "Imports"]
        values = [
            counts["functions"],
            counts["classes"],
            counts["methods"],
            counts["imports"],
        ]

        plt.figure(figsize=(10, 6))
        plt.barh(labels, values, color="#4a90e2")
        plt.xlabel("Count")
        plt.title("Function / Class / Method / Import Distribution")

        for index, value in enumerate(values):
            plt.text(value + 0.1, index, str(value), va='center')

        out = self._ensure_output_dir(project_name)
        plt.savefig(f"{out}/symbol_distribution.png", bbox_inches='tight')
        plt.close()

    # -----------------------------
    # 3. Routes vs JS Functions
    # -----------------------------
    def routes_vs_js(self, project_ir, project_name):
        counts = project_ir.summary()

        labels = ["API Routes", "JS Functions"]
        values = [
            counts["routes"],
            counts["js_functions"],
        ]

        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color=["#ff7f0e", "#1f77b4"])
        plt.ylabel("Count")
        plt.title("Routes vs JS Functions")

        for i, v in enumerate(values):
            plt.text(i, v + 0.1, str(v), ha='center')

        out = self._ensure_output_dir(project_name)
        plt.savefig(f"{out}/routes_vs_js.png", bbox_inches='tight')
        plt.close()

    # -----------------------------
    # 4. API Call Distribution
    # -----------------------------
    def api_calls(self, project_ir, project_name):
        counts = project_ir.summary()

        labels = ["API Calls"]
        values = [counts["api_calls"]]

        plt.figure(figsize=(6, 5))
        plt.bar(labels, values, color="#2ca02c")
        plt.ylabel("Count")
        plt.title("API Call Distribution")

        for i, v in enumerate(values):
            plt.text(i, v + 0.1, str(v), ha='center')

        out = self._ensure_output_dir(project_name)
        plt.savefig(f"{out}/api_calls.png", bbox_inches='tight')
        plt.close()

    # -----------------------------
    # 5. HTML Event Distribution
    # -----------------------------
    def html_events(self, project_ir, project_name):
        counts = project_ir.summary()

        labels = ["HTML Events"]
        values = [counts["html_events"]]

        plt.figure(figsize=(6, 5))
        plt.bar(labels, values, color="#d62728")
        plt.ylabel("Count")
        plt.title("HTML Event Distribution")

        for i, v in enumerate(values):
            plt.text(i, v + 0.1, str(v), ha='center')

        out = self._ensure_output_dir(project_name)
        plt.savefig(f"{out}/html_events.png", bbox_inches='tight')
        plt.close()

    # -----------------------------
    # Generate All Charts
    # -----------------------------
    def generate_all(self, project_ir, project_name):
        self.file_type_pie(project_ir, project_name)
        self.symbol_distribution(project_ir, project_name)
        self.routes_vs_js(project_ir, project_name)
        self.api_calls(project_ir, project_name)
        self.html_events(project_ir, project_name)
