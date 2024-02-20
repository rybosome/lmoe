import argparse
import ollama
import re

from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.experts.refresh import Refresh
from lmoe.framework.expert_registry import ExpertRegistry
from lmoe.framework.model_registry import ModelRegistry
from lmoe.framework.ollama_client import OllamaClient


@inject
@dataclass
class Initialize(Command):

    expert_registry: ExpertRegistry
    model_registry: ModelRegistry
    ollama_client: OllamaClient

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        # Pull base ollama models if needed
        base_models_needed = self.model_registry.base_models_required()
        print("Base Ollama models needed: ", base_models_needed)
        installed_models = self.model_registry.installed_ollama_model_names()
        for base_model in base_models_needed:
            if base_model in installed_models:
                print(f"  {base_model} already installed")
            else:
                print(f"  Pulling {base_model} from Ollama")
                stream = self.ollama_client.install_ollama_model(base_model)
                for chunk in stream:
                    print("    ", chunk)

        # Refresh (create or delete/recreate) lmoe models, which are modifications of ollama models.
        print("Refreshing Ollama's models: ", self.model_registry.lmoe_model_names())
        self.model_registry.refresh()
