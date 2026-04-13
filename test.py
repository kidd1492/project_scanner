from core.trace.trace_resolver import _get_files
from core.ir_system.ir_reader import load_ir, list_files



if __name__ == "__main__":
    project_name = "project_scanner"
    ir = load_ir(project_name)
    files = list_files(ir)

    for file in files:
        print(file.get(""))
    
    #files = _get_files(ir)
    #print(files)