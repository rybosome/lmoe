from lmoe.definitions import (
    get_template_file_names,
    get_project_version,
    get_pyproject_filename,
)
from setuptools import setup, find_packages


setup(
    name="lmoe",
    version=get_project_version(),
    packages=find_packages(),
    package_data={"lmoe": get_template_file_names() + [get_pyproject_filename()]},
    include_package_data=True,
)
