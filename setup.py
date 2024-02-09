import lmoe.experts

from lmoe.framework.expert_registry import ExpertRegistry
from setuptools import setup, find_packages


setup(
    name="lmoe",
    version="0.3.0",
    packages=find_packages(),
    package_data={"lmoe": ExpertRegistry.modelfile_names()},
)
