from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert
from lmoe.utils.templates import (
    Example,
    read_template,
    read_yaml_examples,
    render_examples,
)
from string import Template

import ollama


@expert
class Personality(BaseExpert):

    def __init__(self):
        self.examples = read_yaml_examples("personality.examples.yaml")

    @classmethod
    def name(cls):
        return "PERSONALITY"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "A personality generator, who will use general knowledge and information provided by the user to answer their queries in a fun way, implementing a fun personality for the character Lmoe Armadillo."

    def example_queries(self):
        return [example.user_query for example in self.examples]

    def modelfile_contents(self):
        modelfile_template = Template(read_template(self.modelfile_name()))
        return modelfile_template.substitute(
            all_examples=render_examples(self.examples)
        )

    def generate(self, lmoe_query: LmoeQuery):
        stream = ollama.generate(
            model="lmoe_personality",
            prompt=lmoe_query.render(),
            stream=True,
        )
        for chunk in stream:
            if chunk["response"] or not chunk["done"]:
                print(chunk["response"], end="", flush=True)
        print("")
