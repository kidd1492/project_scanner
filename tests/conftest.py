import os
import tempfile
import shutil
import pytest

@pytest.fixture
def temp_project_dir():
    """Creates a temporary project directory with sample files."""
    temp_dir = tempfile.mkdtemp()

    # Python file
    with open(os.path.join(temp_dir, "sample.py"), "w") as f:
        f.write("def hello():\n    return 'world'\n")

    # HTML file
    with open(os.path.join(temp_dir, "index.html"), "w") as f:
        f.write("<button onclick=\"doThing()\">Click</button>")

    # JS file
    with open(os.path.join(temp_dir, "script.js"), "w") as f:
        f.write("function doThing() { fetch('/api'); }")

    yield temp_dir
    shutil.rmtree(temp_dir)
