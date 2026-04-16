from services.project_service import ProjectService

def test_project_service_loads_project(temp_project_dir):
    service = ProjectService()
    ir = service.load_project(temp_project_dir)

    assert ir.total_files == 3
