from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery

import ollama


class Code(BaseExpert):

    @classmethod
    def name(cls):
        return "CODE"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "A model specifically for generating code. It is expected that this is an instruction-tuned model rather than a 'fill in the middle' model, meaning that a user will describe a coding task or coding question in natural language rather than supplying code and expecting the following code to be generated."

    def examples(self):
        return [
            "write a python script which determines the largest directory in my home environment",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        stream = ollama.generate(
            model="lmoe_code",
            prompt=lmoe_query.render(),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
