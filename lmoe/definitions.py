import importlib.metadata
import importlib.resources
import os


def get_template_module():
    """The module string within which all of the template resource files reside."""
    return "lmoe.templates"


def get_project_version():
    """Returns the semantic versioning string associated with this project."""
    return importlib.metadata.version("lmoe")


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
