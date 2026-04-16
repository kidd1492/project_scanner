from core.analyzers.js_analyzer import JSAnalyzer

def test_js_analyzer_extracts_js_functions(temp_project_dir):
    analyzer = JSAnalyzer()
    file = f"{temp_project_dir}/script.js"

    ir_file = analyzer.analyze_file(file)

    assert len(ir_file.js_functions) == 1
    func = ir_file.js_functions[0]
    assert func.name == "doThing"
    assert func.api_call.startswith("fetch")
