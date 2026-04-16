from core.trace.trace_builder import TraceBuilder

def test_trace_builder_creates_tree():
    builder = TraceBuilder()
    tree = builder.build_trace("dummy", "trigger")
    assert tree is not None
