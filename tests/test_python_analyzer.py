from core.analyzers.python_analyzer import PythonAnalyzer

def test_python_analyzer_extracts_function(temp_project_dir):
    analyzer = PythonAnalyzer()
    file = f"{temp_project_dir}/sample.py"

    ir_file = analyzer.analyze_file(file)

    assert len(ir_file.functions) == 1
    assert ir_file.functions[0].name == "hello"
