# infrastructure/ir_cache.py

import os
from utilities.file_handling import open_json

class IRCache:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load(self, project_name):
        project_dir = os.path.join(self.data_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")

        if not os.path.exists(project_file):
            return None

        return open_json(project_file)

    def exists(self, project_name):
        project_dir = os.path.join(self.data_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")
        return os.path.exists(project_file)

'''
import os
from utilities.file_handling import open_json

class IRCache:
    def __init__(self, cache_dir="data"):
        self.cache_dir = cache_dir

    def load(self, project_name):
        project_dir = os.path.join(self.cache_dir, project_name)
        project_file = os.path.join(project_dir, f"{project_name}.json")

        if not os.path.exists(project_file):
            return None

        return open_json(project_file)

    def exists(self, project_name):
        project_dir = os.path.join(self.cache_dir, project_name)
        return os.path.exists(project_dir)
'''
        