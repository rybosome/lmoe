from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.api.model_expert import ModelExpert
from lmoe.framework.expert_registry import expert
from lmoe.framework.ollama_client import OllamaClient

import ollama


@expert
class General(ModelExpert):

    @inject
    def __init__(self, ollama_client: OllamaClient):
        self._ollama_client = ollama_client
        super(General, self).__init__()

    @classmethod
    def name(cls):
        return "GENERAL"

    def description(self):
        return "An all-purpose model, to be used if a question is asked which requires general knowledge, or if you cannot determine a more specific model that would be more appropriate."

    def example_queries(self):
        return [
            "what is the last item in the list?",
            "What is the distance between Earth and Mars?",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        self._ollama_client.stream(model=self.model(), prompt=lmoe_query)
