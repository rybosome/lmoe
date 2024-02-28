from dataclasses import dataclass
from injector import inject
from lmoe.api.model_expert import ModelExpert
from lmoe.api.model import Model
from lmoe.experts.general import General
from lmoe.framework.expert_registry import ExpertRegistry, expert
from lmoe.framework.lmoe_logger import LogFactory
from lmoe.utils.templates import read_template
from typing import List
from string import Template

import re
import ollama


_EXAMPLE_TEMPLATE = Template(
    """
<start_of_turn>user
$example_query
<end_of_turn>
<start_of_turn>model
$expert_type
<end_of_turn>
"""
)


_PROMPT_TEMPLATE = Template(
    """
<start_of_turn>user
$user_query
<end_of_turn>
<start_of_turn>model
"""
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
        modelfile_template = read_template(self.modelfile_name())
        return modelfile_template.substitute(
            base_ollama_model=self.parent_ollama_name(),
            all_experts=all_experts,
            all_experts_with_descriptions=all_experts_with_descriptions,
            all_examples="\n".join(examples),
        )


@expert
class Classifier(ModelExpert):

    @inject
    def __init__(
        self,
        expert_registry: ExpertRegistry,
        model: ClassifierModel,
        log_factory: LogFactory,
    ):
        self.expert_registry = expert_registry
        self.logger = log_factory.logger(__name__)
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
        self.logger.debug(f"Classifying user query: {user_query}")
        model_response = ollama.generate(
            model=self.model().ollama_name(),
            prompt=_PROMPT_TEMPLATE.substitute(user_query=user_query),
        )
        unescaped_model_response = model_response["response"].replace(r"\_", "_")
        self.logger.debug(f"Unescaped model response: {unescaped_model_response}")
        for name in self.expert_registry.names():
            match = re.match(f"^[\s]*{name}.*", unescaped_model_response)
            if match:
                self.logger.debug(f"Classification: {name}")
                return name
        self.logger.debug(
            f"Could not match model classification: {unescaped_model_response}"
        )
        self.logger.debug("Using GENERAL")
        return General.name()
