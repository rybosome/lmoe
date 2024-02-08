from setuptools import setup, find_packages

from lmoe.framework.expert_registry import get_all_modelfile_names

setup(
    name="lmoe",
    version="0.2.1",
    packages=find_packages(),
    package_data={"lmoe": get_all_modelfile_names()},
)
