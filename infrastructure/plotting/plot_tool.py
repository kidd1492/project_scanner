import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

class PlotTool:
    def __init__(self, base_dir="web_app/static/projects"):
        self.base_dir = base_dir

    def _ensure_output_dir(self, project_name):
        path = os.path.join(self.base_dir, project_name)
        os.makedirs(path, exist_ok=True)
        return path

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

    # ...repeat for the other charts...

    def generate_all(self, project_ir, project_name):
        self.file_type_pie(project_ir, project_name)
        # ...other charts...
