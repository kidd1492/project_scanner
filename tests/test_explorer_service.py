from services.explorer_service import ExplorerService
from infrastructure.ir_cache import IRCache

def test_explorer_lists_files(temp_project_dir):
    cache = IRCache()
    service = ExplorerService(cache)

    files = service.list_project_files(temp_project_dir)
    assert len(files) == 3
