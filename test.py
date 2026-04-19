from core.ir_system.typed_ir.ir_class import IRClass
from infrastructure.typed_ir_cache import TypedIRCache
#print(type(ir))

class AnalysisService:
    def __init__(self, typed_ir_cache):
        self.typed_ir_cache = typed_ir_cache
        self.files = self.typed_ir_cache.files

    def get_python_files(self):
        return [f for f in self.files if f.path.endswith(".html")]



if __name__ == "__main__":
    ir = TypedIRCache().load("project_scanner")
    graph_service = AnalysisService(ir)

    js_files = graph_service.get_python_files()
    print(js_files[0].source)





    '''
    py_files = file_service.get_python_files()

    one = py_files[12].classes[0]
    print(f"class name : {one.name}")
    methods = one.get_methods()
    [print(f"{m.name}") for m in methods]

    print(methods[1])
    print()
    print(py_files[12].source)

    
    js_analyzer = ir.get_file_by_symbol("project_ir.py::ProjectIR")
    methods = js_analyzer.classes[0].methods
    #[print(f"{m.name} : {m.args}") for m in methods]

    routes = ir.get_routes()
    [print(f"name : {r.name} route: {r.route} id: {r.symbol_id}") for r in routes]
    '''

    
'''
def who_called(project_name, function_name):
    ir = load_ir(project_name)["ir"]["files"]
    #print(ir.keys())

    python_files = []
    callers = []
    for file in ir:
        if file["type"] == "py":
            python_files.append(file)

    for python_file in python_files:
        functions = python_file["functions"]
        api_calls = python_file["api_calls"]

        for funct in functions:
            if function_name in funct["calls"]:
                callers.append(funct)

        for f in api_calls:
            if f in api_calls["calls"]:
                callers.append(f)
    return callers
'''
