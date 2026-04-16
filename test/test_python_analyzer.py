from core.analyzers.python_analyzer import PythonAnalyzer

def test_python_analyzer_extracts_functions(temp_project_dir):
    analyzer = PythonAnalyzer()
    sample_file = f"{temp_project_dir}/sample.py"

    ir_file = analyzer.analyze_file(sample_file)

    assert ir_file is not None
    assert len(ir_file.functions) == 1
    assert ir_file.functions[0].name == "hello"
