from lmoe.api.base_expert import BaseExpert
from string import Template

import ollama

_PROMPT_TEMPLATE = Template(
    """
===user-context===
$user_context
===user-context===
===user-query===
$user_query
===user-query===
-response-
"""
)


class ProjectInitialization(BaseExpert):

    @classmethod
    def name(cls):
        return "PROJECT_INITIALIZATION"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "A model designed to initialize programming projects. Given verbal and ascii art descriptions and context, initializes programming projects in a number of different languages."

    def examples(self):
        return [
            "what is the recommended layout for a python project with poetry",
            "create a project for a java webserver using spring to serve the contents of the '/web/ directory",
            "initialize a project for a new npm module",
            "create a project like this",
            "make a project like this one",
        ]

    def generate(self, user_context, user_query):
        stream = ollama.generate(
            model="lmoe_project_initialization",
            prompt=_PROMPT_TEMPLATE.substitute(
                user_context=user_context, user_query=user_query
            ),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
