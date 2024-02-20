import ollama

from injector import inject
from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert
from lmoe.framework.model_registry import ModelRegistry


@expert
class Refresh(BaseExpert):

    @inject
    def __init__(self, model_registry: ModelRegistry):
        self.model_registry = model_registry

    @classmethod
    def name(cls):
        return "REFRESH"

    @classmethod
    def has_model(cls):
        return False

    def description(self):
        return "An internal command to refresh internal lmoe modelfiles, which is necessary after adding new ones or modifying a prompt."

    def example_queries(self):
        return [
            "refresh",
            "refresh classifier",
            "classifier refresh",
            "update modelfiles",
            "update models",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        print("Refreshing Ollama's models: ", self.model_registry.lmoe_model_names())
        self.model_registry.refresh()
