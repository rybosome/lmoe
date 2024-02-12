from lmoe.api.lmoe_query import LmoeQuery
from lmoe.api.model_expert import ModelExpert
from lmoe.api.ollama_client import stream
from lmoe.framework.expert_registry import expert

import ollama


@expert
class ProjectInitialization(ModelExpert):

    @classmethod
    def name(cls):
        return "PROJECT_INITIALIZATION"

    def description(self):
        return "A model designed to initialize programming projects. Given verbal and ascii art descriptions and context, initializes programming projects in a number of different languages. Does not answer questions about how to initialize, only commands to perform initialization."

    def example_queries(self):
        return [
            "create a project for a java webserver using spring to serve the contents of the '/web/ directory",
            "initialize a project for a new npm module",
            "create a project like this",
            "make a project like this one",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        for chunk in stream(model=self.model, prompt=lmoe_query):
            print(chunk, end="", flush=True)
        print("")
