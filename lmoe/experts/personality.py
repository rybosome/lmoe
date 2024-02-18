from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.api.model import Model
from lmoe.api.model_expert import ModelExpert
from lmoe.framework.expert_registry import expert
from lmoe.framework.ollama_client import OllamaClient
from lmoe.utils.templates import (
    Example,
    read_template,
    read_yaml_examples,
    render_examples,
)
from string import Template

import ollama


class PersonalityModel(Model):

    def __init__(self):
        self.examples = read_yaml_examples("personality.examples.yaml")
        super(PersonalityModel, self).__init__("PERSONALITY")

    def modelfile_contents(self):
        modelfile_template = Template(read_template(self.modelfile_name()))
        return modelfile_template.substitute(
            all_examples=render_examples(self.examples)
        )


# @expert
class Personality(ModelExpert):

    @inject
    def __init__(self, ollama_client: OllamaClient):
        self.examples = read_yaml_examples("personality.examples.yaml")
        self._ollama_client = ollama_client
        super(Personality, self).__init__(PersonalityModel())

    @classmethod
    def name(cls):
        return "PERSONALITY"

    def description(self):
        return "A personality generator, who will use general knowledge and information provided by the user to answer their queries in a fun way, implementing a fun personality for the character Lmoe Armadillo."

    def example_queries(self):
        return [example.user_query for example in self.examples]

    def generate(self, lmoe_query: LmoeQuery):
        self._ollama_client.stream(model=self.model(), prompt=lmoe_query)
