from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery

import ollama



class General(BaseExpert):

    @classmethod
    def name(cls):
        return "GENERAL"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "An all-purpose model, to be used if a question is asked which requires general knowledge, or if you cannot determine a more specific model that would be more appropriate."

    def examples(self):
        return [
            "what is the last item in the list?",
            "What are you?",
            "What is the distance between Earth and Mars?",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        stream = ollama.generate(
            model="lmoe_general",
            prompt=lmoe_query.render(),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
