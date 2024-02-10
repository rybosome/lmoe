import importlib.resources
import os

VERSION = "0.3.0"

TEMPLATE_MODULE = "lmoe.templates"

# Object containing the template directory
TEMPLATE_DIR_OBJECT = importlib.resources.files(TEMPLATE_MODULE)

# The absolute template path
TEMPLATE_DIR_PATH = TEMPLATE_DIR_OBJECT.name

# Mapping from filename to Traversable object
TEMPLATES = {
    file_object.name: file_object for file_object in TEMPLATE_DIR_OBJECT.iterdir()
}

# The absolute filenames of all resource template files
TEMPLATE_FILE_NAMES = [
    os.path.join(TEMPLATE_DIR_PATH, template_filename)
    for template_filename in TEMPLATES.keys()
]
