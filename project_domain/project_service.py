# project_service.py

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
    # Get a single ProjectIR
    # -----------------------------
    def get_project(self, project_name):
        return self.persistance.load(project_name)

    # -----------------------------
    # Scan a project
    # -----------------------------
    def scan_project(self, path):
        """
        Route layer already validated:
        - path exists
        - not duplicate
        """
        file_list = self.discover_files(path)
        project_ir = self.analyzer_manager.run_analyzers(file_list, path)
        self.persistance.save(project_ir)
        return project_ir

    # -----------------------------
    # Build DashboardIR
    # -----------------------------
    def get_dashboard(self, project_name):
        project_ir = self.persistance.load(project_name)
        if not project_ir:
            return None
        return self.dashboard_builder.build_dashboard(project_ir)
