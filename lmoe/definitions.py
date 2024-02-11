import importlib.resources
import os
import toml
import pathlib

TEMPLATE_MODULE = "lmoe.templates"

# Object containing the template directory
TEMPLATE_DIR_OBJECT = importlib.resources.files(TEMPLATE_MODULE)

# The absolute template path
TEMPLATE_DIR_PATH = TEMPLATE_DIR_OBJECT.name

_PYPROJECT_DATA = None


def get_project_data():
    global _PYPROJECT_DATA 
    if _PYPROJECT_DATA  is None:
        pyproject_path = pathlib.Path(__file__).parent.parent / 'pyproject.toml'
        with open(pyproject_path, 'r') as file:
            _PYPROJECT_DATA = toml.load(file)
    return _PYPROJECT_DATA

def get_project_version():
    return get_project_data()["tool"]["poetry"]["version"]


# Mapping from filename to Traversable object
TEMPLATES = {
    file_object.name: file_object for file_object in TEMPLATE_DIR_OBJECT.iterdir()
}

# The absolute filenames of all resource template files
_TEMPLATE_FILE_NAMES = None

def get_template_file_names():
    if _TEMPLATE_FILE_NAMES is None:
        _TEMPLATE_FILE_NAMES = [
            os.path.join(TEMPLATE_DIR_PATH, template_filename)
            for template_filename in TEMPLATES.keys()
        ]
    return _TEMPLATE_FILE_NAMES
