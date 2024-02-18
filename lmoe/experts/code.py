from injector import inject
from lmoe.api.model_expert import ModelExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.ollama_client import OllamaClient
from lmoe.framework.expert_registry import expert


@expert
class Code(ModelExpert):

    @inject
    def __init__(self, ollama_client: OllamaClient):
        self._ollama_client = ollama_client
        super(Code, self).__init__()

    @classmethod
    def name(cls):
        return "CODE"

    def description(self):
        return "A model specifically for generating code. It is expected that this is an instruction-tuned model rather than a 'fill in the middle' model, meaning that a user will describe a coding task or coding question in natural language rather than supplying code and expecting the following code to be generated."

    def example_queries(self):
        return [
            "write a python script which determines the largest directory in my home environment",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        self._ollama_client.stream(self.model(), lmoe_query)
