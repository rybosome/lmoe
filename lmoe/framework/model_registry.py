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

    def lmoe_model_names(self) -> Set[str]:
        return set(
            [
                e.model().ollama_name()
                for e in self.expert_registry.experts()
                if e.has_model()
            ]
        )

    def installed_ollama_model_names(self) -> Set[str]:
        """The set of underlying models currently installed in ollama."""
        return set(
            [
                model.name.split(":")[0]
                for model in self.ollama_client.installed_models()
            ]
        )

    def refresh(self):
        """Ensures that all installed models match their modelfile configuration."""
        existing_model_names = self.installed_ollama_model_names()
        for model in [
            e.model() for e in self.expert_registry.experts() if e.has_model()
        ]:
            if model.ollama_name() in existing_model_names:
                self.ollama_client.delete_ollama_model(model.ollama_name())
            self.ollama_client.create_ollama_model(
                model_name=model.ollama_name(),
                modelfile_contents=model.modelfile_contents(),
            )
