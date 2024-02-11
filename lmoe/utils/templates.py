import importlib.resources
import yaml

from dataclasses import dataclass
from lmoe.definitions import get_template_module
from string import Template
from typing import List, Optional

# Mapping from filename to Traversable object
_TEMPLATES = None


def load_templates():
    global _TEMPLATES
    if _TEMPLATES is None:
        template_dir_object = importlib.resources.files(get_template_module())
        _TEMPLATES = {
            file_object.name: file_object
            for file_object in template_dir_object.iterdir()
        }
    return _TEMPLATES


def read_template(filename):
    templates = load_templates()
    if not filename in templates:
        raise Exception("Could not find: " + filename)
    template = templates[filename]
    return template.read_text()


def read_yaml_file(filename):
    templates = load_templates()
    if not filename in templates:
        raise Exception("Could not find: " + filename)
    yaml_file = templates[filename]
    return yaml.safe_load(yaml_file.read_text())


@dataclass
class Example:
    """Example user context, query, and response."""

    stdin_context: Optional[str]
    paste_context: Optional[str]
    user_query: Optional[str]
    agent_response: Optional[str]


def read_yaml_examples(filename):
    """Reads a yaml file as a list of lmoe.utils.templates.Example instances."""
    return [Example(**example_dict) for example_dict in read_yaml_file(filename)]


_EXAMPLE_TEMPLATE = Template(
    """
Example $example_index)

===stdin-context===
$stdin_context
===stdin-context===
===paste-context===
$paste_context
===paste-context===
===user-query===
$user_query
===user-query===
$agent_response
"""
)


def render_examples(examples) -> str:
    rendered_examples = []
    example_index = 0
    for example in examples:
        example_index += 1
        rendered_examples.append(
            _EXAMPLE_TEMPLATE.substitute(
                example_index=example_index,
                stdin_context=example.stdin_context,
                paste_context=example.paste_context,
                user_query=example.user_query,
                agent_response=example.agent_response,
            )
        )
    return "\n\n".join(rendered_examples)
