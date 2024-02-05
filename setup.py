from setuptools import setup, find_packages

from lmoe.experts.expert_registry import get_all_modelfile_names

setup(
    name="lmoe",
    version="0.1.2",
    packages=find_packages(),
    package_data={"lmoe": get_all_modelfile_names()},
)
