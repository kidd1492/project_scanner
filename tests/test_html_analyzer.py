from core.analyzers.html_analyzer import HTMLAnalyzer

def test_html_analyzer_extracts_events(temp_project_dir):
    analyzer = HTMLAnalyzer()
    file = f"{temp_project_dir}/index.html"

    ir_file = analyzer.analyze_file(file)

    assert len(ir_file.html_events) == 1
    event = ir_file.html_events[0]
    assert event.name == "doThing"
    assert event.event == "onclick"
