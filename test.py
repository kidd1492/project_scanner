from services.trace_service import load_ir
#from core.ir_system.ir_reader import load_ir


def compair_ir(project_name):
    ir_reader = load_ir(project_name)
    one = ir_reader.keys()
    return one



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


if __name__ == "__main__":
    project_name = "project_scanner"
    function_name = 'load_ir'

    #ir_reader = compair_ir(project_name)
    #print(ir_reader)
    
    callers = who_called(project_name, function_name)

    for item in callers:
        print(f"called by : {item['name']}\nfrom : {item['file']}\n")
    

