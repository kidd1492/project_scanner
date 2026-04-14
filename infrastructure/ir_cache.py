class IRCache:
    def __init__(self, loader):
        self.loader = loader
        self._cache = {}

    def get(self, project_name):
        if project_name not in self._cache:
            self._cache[project_name] = self.loader(project_name)
        return self._cache[project_name]

    def invalidate(self, project_name):
        self._cache.pop(project_name, None)
