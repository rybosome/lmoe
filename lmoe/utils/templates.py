import pkg_resources

_TEMPLATE_PATH = "lmoe/experts/templates/"


def template_path():
    return _TEMPLATE_PATH


def read_template(filename):
    template_path = pkg_resources.resource_filename(
        __name__, f"../../{_TEMPLATE_PATH}{filename}"
    )
    try:
        with open(template_path, "r") as file:
            template_contents = file.read()
        return template_contents
    except FileNotFoundError:
        return f"Template file not found: {template_path}"
