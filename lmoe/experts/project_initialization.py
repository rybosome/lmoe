from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery

import ollama


class ProjectInitialization(BaseExpert):

    @classmethod
    def name(cls):
        return "PROJECT_INITIALIZATION"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "A model designed to initialize programming projects. Given verbal and ascii art descriptions and context, initializes programming projects in a number of different languages. Does not answer questions about how to initialize, only commands to perform initialization."

    def examples(self):
        return [
            "create a project for a java webserver using spring to serve the contents of the '/web/ directory",
            "initialize a project for a new npm module",
            "create a project like this",
            "make a project like this one",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        stream = ollama.generate(
            model="lmoe_project_initialization",
            prompt=lmoe_query.render(),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
