from string import Template

from lmoe.api.base_expert import BaseExpert
from lmoe.framework import expert_registry

import ollama


class Refresh(BaseExpert):

    @classmethod
    def name(cls):
        return "REFRESH"

    @classmethod
    def has_modelfile(cls):
        return False

    def description(self):
        return "An internal command to refresh internal lmoe modelfiles, which is necessary after adding new ones or modifying a prompt."

    def examples(self):
        return [
            "refresh",
            "refresh classifier",
            "classifier refresh",
            "update modelfiles",
            "update models",
        ]

    def generate(self, user_context, user_query):
        response = ollama.list()
        existing_model_names = [
            model["name"].split(":")[0] for model in response["models"]
        ]
        for e in [e for e in expert_registry.values() if e.has_modelfile()]:
            if e.model_name() in existing_model_names:
                print(f"Deleting existing {e.model_name()}...")
                ollama.delete(e.model_name())
            print(f"Updating {e.model_name()}...")
            ollama.create(model=e.model_name(), modelfile=e.modelfile_contents())
