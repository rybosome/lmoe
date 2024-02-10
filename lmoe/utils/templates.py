import yaml

from dataclasses import dataclass
from definitions import TEMPLATES
from string import Template
from typing import List, Optional


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


def read_template(filename):
    if not filename in TEMPLATES:
        raise Exception("Could not find: " + filename)
    template = TEMPLATES[filename]
    return template.read_text()


def read_yaml_file(filename):
    if not filename in TEMPLATES:
        print(TEMPLATES)
        raise Exception("Could not find: " + filename)
    yaml_file = TEMPLATES[filename]
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
