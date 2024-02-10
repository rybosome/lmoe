from string import Template
from lmoe.api.base_expert import BaseExpert
from lmoe.experts.general import General
from lmoe.utils.templates import read_template
from injector import inject
from lmoe.framework.expert_registry import ExpertRegistry
from typing import List
from lmoe.framework.expert_registry import expert

import re
import ollama


_EXAMPLE_TEMPLATE = Template(
    """
Example $example_index)

===user-query===
$example_query
===user-query===
$expert_type
"""
)


_PROMPT_TEMPLATE = Template(
    """
===user-query===
$user_query
===user-query===
"""
)


@expert
class Classifier(BaseExpert):

    @inject
    def __init__(self, expert_registry: ExpertRegistry):
        self.expert_registry = expert_registry

    @classmethod
    def name(cls):
        return "CLASSIFIER"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "The top-level query classifier for lmoe, a layered mixture of experts. Determines from a user's query the expert, LLM or multimodal model which would best serve the user's needs."

    def non_self_expert_names(self) -> List[str]:
        return [name for name in ExpertRegistry.names() if name != Classifier.name()]

    def non_self_experts(self):
        return [
            expert
            for expert in self.expert_registry.experts()
            if expert.name() != Classifier.name()
        ]

    def example_queries(self):
        all_example_queries = []
        for e in self.non_self_experts():
            example_queries.extend(e.examples())
        return all_example_queries

    def modelfile_contents(self):
        all_experts = ", ".join(self.non_self_expert_names())
        all_experts_with_descriptions = "\n".join(
            [
                Template("$name: $description").substitute(
                    name=e.name(), description=e.description()
                )
                for e in self.non_self_experts()
            ]
        )
        examples = []
        example_index = 1
        for e in self.non_self_experts():
            for example_query in e.example_queries():
                examples.append(
                    _EXAMPLE_TEMPLATE.substitute(
                        example_index=example_index,
                        example_query=example_query,
                        expert_type=e.name(),
                    )
                )
                example_index += 1
        modelfile_template = Template(read_template(self.modelfile_name()))
        return modelfile_template.substitute(
            all_experts=all_experts,
            all_experts_with_descriptions=all_experts_with_descriptions,
            all_examples="\n\n".join(examples),
        )

    def classify(self, user_query):
        response = ollama.generate(
            model="lmoe_classifier",
            prompt=_PROMPT_TEMPLATE.substitute(user_query=user_query),
        )
        return self._parse(response["response"])

    def _parse(self, model_response):
        unescaped_model_response = model_response.replace(r"\_", "_")
        for name in ExpertRegistry.names():
            match = re.match(f"^[\s]*{name}.*", unescaped_model_response)
            if match:
                return name
        return General.name()
