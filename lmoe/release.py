import os
import pathlib
import re

from lmoe.definitions import get_project_version


def update_readme_version():
    # Get project version
    project_version = get_project_version()

    # Update README.md in the project root
    readme_path = pathlib.Path(__file__).parent.parent / "README.md"
    update_version_in_file(readme_path, project_version)

    # Update README.md in the docs directory
    docs_readme_path = pathlib.Path(__file__).parent.parent / os.path.join(
        "docs", "README.md"
    )
    update_version_in_file(docs_readme_path, project_version)


def update_version_in_file(file_path, version):
    with open(file_path, "r") as file:
        content = file.read()

    # Replace version string
    updated_content = re.sub(
        r"Version[0-9]+\.[0-9]+\.[0-9]+", f"Version {version}", content
    )

    with open(file_path, "w") as file:
        file.write(updated_content)

    print(f"Updated {file_path} with version {version}.")
