from core.ir_system.builder import build_project_ir
from core.ir_system.typed_ir import ProjectIR, IRFile

def test_build_project_ir(temp_project_dir):
    ir: ProjectIR = build_project_ir(temp_project_dir)

    assert isinstance(ir, ProjectIR)
    assert ir.total_files == 1
    assert len(ir.files) == 1

    file_ir: IRFile = ir.files[0]
    assert file_ir.path.endswith("sample.py")
    assert file_ir.type == "py"
