import os
import tempfile
import shutil
import pytest

@pytest.fixture
def temp_project_dir():
    """Creates a temporary project directory with sample Python files."""
    temp_dir = tempfile.mkdtemp()

    sample_file = os.path.join(temp_dir, "sample.py")
    with open(sample_file, "w") as f:
        f.write("""
def hello():
    return "world"
""")

    yield temp_dir
    shutil.rmtree(temp_dir)
