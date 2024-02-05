from lmoe.api.base_expert import BaseExpert
from string import Template

import ollama

_PROMPT_TEMPLATE = Template(
    """
===user-context===
$user_context
===user-context===
===user-query===
$user_query
===user-query===
-response-
"""
)


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

    def generate(self, user_context, user_query):
        stream = ollama.generate(
            model="lmoe_general",
            prompt=_PROMPT_TEMPLATE.substitute(
                user_context=user_context, user_query=user_query
            ),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
