from definitions import TEMPLATE_FILE_NAMES, VERSION

from setuptools import setup, find_packages


setup(
    name="lmoe",
    version=VERSION,
    packages=find_packages(),
    package_data={"lmoe": TEMPLATE_FILE_NAMES},
)
