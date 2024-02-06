from lmoe.api.base_expert import BaseExpert

import ollama


class ListModels(BaseExpert):

    @classmethod
    def name(cls):
        return "LIST_MODELS"

    @classmethod
    def has_modelfile(cls):
        return False

    def description(self):
        return "Describes lmoe-specific models currently installed."

    def examples(self):
        return [
            "list models",
            "list your models",
            "show models",
            "what are your models?",
            "what are the local models",
            "what models are you using?",
        ]

    def generate(self, user_context, user_query):
        response = ollama.list()
        for model in response['models']:
            if model['name'].startswith('lmoe'):
                print(model)
