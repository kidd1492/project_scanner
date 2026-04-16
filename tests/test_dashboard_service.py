from services.dashboard_service import DashboardService
from infrastructure.ir_cache import IRCache

def test_dashboard_counts(temp_project_dir):
    cache = IRCache()
    service = DashboardService(cache)

    counts = service.get_counts(temp_project_dir)

    assert "total_files" in counts
    assert counts["total_files"] == 3
