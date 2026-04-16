from core.trace.trace_resolver import TraceResolver

def test_trace_resolver_basic():
    resolver = TraceResolver()
    result = resolver.resolve("dummy", "trigger")
    assert result is not None
