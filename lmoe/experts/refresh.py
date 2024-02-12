from injector import inject
from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import ExpertRegistry, expert
from string import Template


import ollama


@expert
class Refresh(BaseExpert):

    @inject
    def __init__(self, expert_registry: ExpertRegistry):
        self.expert_registry = expert_registry

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
        response = ollama.list()
        existing_model_names = [
            model["name"].split(":")[0] for model in response["models"]
        ]
        all_lmoe_models = set(
            [
                e.model.ollama_name()
                for e in self.expert_registry.experts()
                if e.has_model()
            ]
        )
        print("Refreshing Ollama's models: ", all_lmoe_models)
        for model in [e.model for e in self.expert_registry.experts() if e.has_model()]:
            print(f"  {model.ollama_name()}")
            if model.ollama_name() in existing_model_names:
                print(f"    Deleting...")
                ollama.delete(model.ollama_name())
            print(f"    Creating...")
            ollama.create(
                model=model.ollama_name(), modelfile=model.modelfile_contents()
            )
