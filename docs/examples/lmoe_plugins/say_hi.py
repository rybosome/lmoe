from injector import inject
from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.experts.personality import Personality
from lmoe.framework.expert_registry import expert


@expert
class SayHi(BaseExpert):

    @inject
    def __init__(self, personality: Personality):
        self.personality = personality

    @classmethod
    def name(cls):
        return "SAY_HI"

    @classmethod
    def has_model(cls):
        return False

    def description(self):
        return "Returns a friendly greeting from lmoe."

    def example_queries(self):
        return [
            "say hello",
            "introduce yourself",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        print("Hello from a plugin!")
        self.personality.generate(lmoe_query)
