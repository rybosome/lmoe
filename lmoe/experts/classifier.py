from string import Template
from lmoe.framework import expert_registry
from lmoe.api.base_expert import BaseExpert
from lmoe.utils.templates import read_template

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


class Classifier(BaseExpert):

    @classmethod
    def name(cls):
        return "CLASSIFIER"

    @classmethod
    def has_modelfile(cls):
        return True

    def description(self):
        return "The top-level query classifier for lmoe, a layered mixture of experts. Determines from a user's query the expert, LLM or multimodal model which would best serve the user's needs."

    def examples(self):
        example_queries = []
        for e in get_non_self_experts():
            example_queries.extend(e.examples())
        return example_queries

    def get_non_self_expert_names(self):
        return [e.name() for e in expert_registry.values() if e is not self]

    def get_non_self_experts(self):
        return [e for e in expert_registry.values() if e is not self]

    def modelfile_contents(self):
        all_experts = ", ".join(self.get_non_self_expert_names())
        all_experts_with_descriptions = "\n".join(
            [
                Template("$name: $description").substitute(
                    name=e.name(), description=e.description()
                )
                for e in self.get_non_self_experts()
            ]
        )
        examples = []
        example_index = 1
        for e in self.get_non_self_experts():
            for example_query in e.examples():
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
        expert_name = self._parse(response["response"])
        return expert_registry.get_expert(expert_name)

    def _remove_escape_characters(self, input_string):
        escaped_bytes = bytes(input_string, "utf-8").decode("unicode_escape")
        return escaped_bytes

    def _parse(self, model_response):
        unescaped_model_response = model_response.replace(r"\_", "_")
        for name in expert_registry.get_registered_names():
            match = re.match(f"^[\s]*{name}.*", unescaped_model_response)
            if match:
                return name
        return "GENERAL"
