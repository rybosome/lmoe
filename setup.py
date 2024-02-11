from lmoe.definitions import get_template_file_names, get_project_version
from setuptools import setup, find_packages


setup(
    name="lmoe",
    version=get_project_version(),
    packages=find_packages(),
    package_data={"": ["pyproject.toml"], "lmoe": get_template_file_names()},
)
