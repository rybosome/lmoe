from lmoe.api.model import Model
from lmoe.api.lmoe_query import LmoeQuery
from typing import Iterator, Union

import ollama


def stream(model: Model, prompt: Union[LmoeQuery, str]) -> Iterator[str]:
    stream = ollama.generate(
        model=model.ollama_name(),
        prompt=str(prompt),
        stream=True,
    )
    for chunk in stream:
        if chunk["response"] or not chunk["done"]:
            yield chunk["response"]
