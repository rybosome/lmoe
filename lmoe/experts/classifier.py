from dataclasses import dataclass
from injector import inject
from lmoe.api.model_expert import ModelExpert
from lmoe.api.model import Model
from lmoe.experts.general import General
from lmoe.framework.expert_registry import ExpertRegistry, expert
from lmoe.utils.templates import read_template
from typing import List
from string import Template

import re
import ollama


_EXAMPLE_TEMPLATE = Template(
    """
user: $example_query
agent: $expert_type
"""
)


_PROMPT_TEMPLATE = Template(
    """
user: $user_query
agent: """
)

_WITHOUT_CLASSIFIER = ExpertRegistry.Without(name="CLASSIFIER")


@dataclass
class ClassifierModel(Model):
    """A specialized classifier modelfile with additional templating."""

    @inject
    def __init__(self, expert_registry: ExpertRegistry):
        self.expert_registry = expert_registry
        super(ClassifierModel, self).__init__("CLASSIFIER")

    def modelfile_contents(self):
        all_experts = ", ".join(
            [
                e.name()
                for e in self.expert_registry.experts(without=_WITHOUT_CLASSIFIER)
            ]
        )
        all_experts_with_descriptions = "\n".join(
            [
                Template("$name: $description").substitute(
                    name=e.name(), description=e.description()
                )
                for e in self.expert_registry.experts(without=_WITHOUT_CLASSIFIER)
            ]
        )
        examples = []
        for e in self.expert_registry.experts(without=_WITHOUT_CLASSIFIER):
            for example_query in e.example_queries():
                examples.append(
                    _EXAMPLE_TEMPLATE.substitute(
                        example_query=example_query,
                        expert_type=e.name(),
                    )
                )
        modelfile_template = Template(read_template(self.modelfile_name()))
        return modelfile_template.substitute(
            all_experts=all_experts,
            all_experts_with_descriptions=all_experts_with_descriptions,
            all_examples="\n".join(examples),
        )


@expert
class Classifier(ModelExpert):

    @inject
    def __init__(self, expert_registry: ExpertRegistry, model: ClassifierModel):
        self.expert_registry = expert_registry
        super(Classifier, self).__init__(model)

    @classmethod
    def name(cls):
        return "CLASSIFIER"

    def description(self):
        return "The top-level query classifier for lmoe, a layered mixture of experts. Determines from a user's query the expert, LLM or multimodal model which would best serve the user's needs."

    def example_queries(self):
        all_example_queries = []
        for e in self.expert_registry.experts(without=_WITHOUT_CLASSIFIER):
            all_example_queries.extend(e.example_queries())
        return all_example_queries

    def classify(self, user_query):
        model_response = ollama.generate(
            model=self.model.ollama_name(),
            prompt=_PROMPT_TEMPLATE.substitute(user_query=user_query),
        )
        unescaped_model_response = model_response["response"].replace(r"\_", "_")
        for name in self.expert_registry.names():
            match = re.match(f"^[\s]*{name}.*", unescaped_model_response)
            if match:
                return name
        return General.name()
