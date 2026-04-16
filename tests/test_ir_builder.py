from core.ir_system.builder import build_project_ir
from core.ir_system.typed_ir import ProjectIR, IRFile

def test_ir_builder_creates_project_ir(temp_project_dir):
    ir = build_project_ir(temp_project_dir)

    assert isinstance(ir, ProjectIR)
    assert ir.total_files == 3
    assert len(ir.files) == 3

def test_ir_builder_file_types(temp_project_dir):
    ir = build_project_ir(temp_project_dir)
    types = {f.type for f in ir.files}
    assert types == {"py", "html", "js"}
