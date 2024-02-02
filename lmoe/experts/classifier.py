from lmoe.experts import code
from lmoe.experts import expert_type
from lmoe.experts import general
from lmoe.experts import image
from string import Template

import ollama


_PROMPT_TEMPLATE = Template(
    """
===user-query===
$user_query
===user-query===
"""
)


def classify(user_query):
    response = ollama.generate(
        model="lmoe_classifier",
        prompt=_PROMPT_TEMPLATE.substitute(user_query=user_query),
    )
    e_type = expert_type.ExpertType.parse(response["response"])

    if e_type == expert_type.ExpertType.CODE:
        return code.CodeExpert()
    elif e_type == expert_type.ExpertType.IMAGE:
        return image.ImageExpert()

    return general.GeneralExpert()
