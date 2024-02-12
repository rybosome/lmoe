from lmoe.api.lmoe_query import LmoeQuery
from lmoe.api.model_expert import ModelExpert
from lmoe.api.ollama_client import stream
from lmoe.framework.expert_registry import expert

import ollama


@expert
class General(ModelExpert):

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
        for chunk in stream(model=self.model, prompt=lmoe_query):
            print(chunk, end="", flush=True)
        print("")
