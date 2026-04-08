import os


def get_existing_projects():
    DATA_DIR = "data"
    projects = []

    if os.path.exists(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            full_path = os.path.join(DATA_DIR, name)
            if os.path.isdir(full_path):
                projects.append(name)
    return projects