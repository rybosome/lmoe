from lmoe.experts import expert_type
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


class GeneralExpert:

    @staticmethod
    def expert_type():
        return expert_type.ExpertType.GENERAL

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
