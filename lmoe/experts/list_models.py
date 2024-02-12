from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert

import ollama


@expert
class ListModels(BaseExpert):

    @classmethod
    def name(cls):
        return "LIST_MODELS"

    @classmethod
    def has_model(cls):
        return False

    def description(self):
        return "Describes lmoe-specific models currently installed."

    def example_queries(self):
        return [
            "list models",
            "list your models",
            "show models",
            "what are your models?",
            "what are the local models",
            "what models are you using?",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        response = ollama.list()
        for model in response["models"]:
            if model["name"].startswith("lmoe"):
                print(model)
