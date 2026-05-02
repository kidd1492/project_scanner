class ProjectService:
    def __init__(self, discover_files, analyzer_manager, persistance, dashboard_builder):
        self.discover_files = discover_files
        self.analyzer_manager = analyzer_manager
        self.persistance = persistance
        self.dashboard_builder = dashboard_builder

    # -----------------------------
    # List all projects
    # -----------------------------
    def get_existing_projects(self):
        return self.persistance.list_all_projects()

    # -----------------------------
    # Get a single project
    # -----------------------------
    def get_project(self, project_name):
        project_ir = self.persistance.load(project_name)
        if not project_ir:
            return {"error": "Project not found"}
        return project_ir.to_dict()

    # -----------------------------
    # Scan a project
    # -----------------------------
    def scan_project(self, data):
        path = data.get("path")
        if not path:
            return {"error": "No path provided"}

        if self.persistance.exists(path):
            return {"error": "Project Exist"}

        file_list = self.discover_files(path)
        project_ir = self.analyzer_manager.run_analyzers(file_list, path)
        self.persistance.save(project_ir)

        return project_ir.to_dict()

    # -----------------------------
    # Build DashboardIR
    # -----------------------------
    def get_dashboard(self, project_name):
        project_ir = self.persistance.load(project_name)
        if not project_ir:
            return {"error": "Project not found"}

        dashboard_ir = self.dashboard_builder.build_dashboard(project_ir)
        return dashboard_ir.to_dict()
