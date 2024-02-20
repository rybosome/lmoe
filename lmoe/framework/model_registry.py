import argparse
import re

from dataclasses import dataclass
from injector import inject
from lmoe.framework.expert_registry import ExpertRegistry
from lmoe.framework.ollama_client import OllamaClient
from typing import Set


@inject
@dataclass
class ModelRegistry:

    expert_registry: ExpertRegistry
    ollama_client: OllamaClient

    def base_models_required(self) -> Set[str]:
        """Returns the set of ollama models expressed as dependencies in all known modelfiles."""
        base_models = set()
        for expert in [e for e in self.expert_registry.experts() if e.has_model()]:
            modelfile_contents = expert.model().modelfile_contents()
            match = re.match(r"FROM ([^\s]+).*", modelfile_contents)
            if match:
                base_models.add(match.group(1))
        return base_models

    def installed_ollama_model_names(self) -> Set[str]:
        """The set of underlying models currently installed in ollama."""
        return set(
            [
                model.name.split(":")[0]
                for model in self.ollama_client.installed_models()
            ]
        )
