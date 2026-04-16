from services.trace_service import TraceService
from infrastructure.ir_cache import IRCache

def test_trace_service_triggers(temp_project_dir):
    cache = IRCache()
    service = TraceService(cache)

    triggers = service.get_triggers(temp_project_dir)
    assert isinstance(triggers, list)
