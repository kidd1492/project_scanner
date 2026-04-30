from .dashboard_ir import DashboardIR

class DashboardBuilder:
    def __init__(self, plot_tool=None):
        self.plot_tool = plot_tool

    def build(self, project_ir):
        dashboard_ir = DashboardIR(
            project_name=project_ir.project_name,
            root=project_ir.root,
            total_files=project_ir.total_files,
            file_type_counts=project_ir.count_file_types(),
            symbol_counts=project_ir.count_symbols(),
            routes=project_ir.count_routes(),
            js_functions=project_ir.count_js_functions(),
            html_events=project_ir.count_html_events(),
            api_calls=project_ir.count_api_calls(),
        )

        if self.plot_tool:
            self.plot_tool.generate_all(project_ir, project_ir.project_name)

        return dashboard_ir
