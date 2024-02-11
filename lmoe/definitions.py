import importlib.resources
import os
import toml
import pathlib


def get_template_module():
    """The module string within which all of the template resource files reside."""
    return "lmoe.templates"


def get_pyproject_filename():
    return importlib.resources.files("lmoe").joinpath("pyproject.toml").name


# Cache data for the root pyproject.toml file.
_PYPROJECT_DATA = None


def get_project_data():
    """Return the pyproject.toml file structured as a multi-layer dict.

    Caches loaded data so that this is only retrieved from the filesystem once.
    """
    global _PYPROJECT_DATA
    if _PYPROJECT_DATA is None:
        pyproject_path = importlib.resources.files("lmoe").joinpath("pyproject.toml")
        _PYPROJECT_DATA = toml.loads(pyproject_path.read_text())
    return _PYPROJECT_DATA


def get_project_version():
    """Returns the semantic versioning string associated with this project."""
    return get_project_data()["tool"]["poetry"]["version"]


# The absolute filenames of all resource template files
_TEMPLATE_FILE_NAMES = None


def get_template_file_names():
    global _TEMPLATE_FILE_NAMES
    if _TEMPLATE_FILE_NAMES is None:
        template_dir_object = importlib.resources.files(get_template_module())
        _TEMPLATE_FILE_NAMES = [
            os.path.join(template_dir_object.name, file_object.name)
            for file_object in template_dir_object.iterdir()
        ]
    return _TEMPLATE_FILE_NAMES
