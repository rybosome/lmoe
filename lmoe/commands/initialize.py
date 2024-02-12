import argparse
import ollama
import re

from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.experts.refresh import Refresh
from lmoe.framework.expert_registry import ExpertRegistry


@inject
@dataclass
class Initialize(Command):

    expert_registry: ExpertRegistry
    refresh: Refresh

    def _get_all_base_models(self):
        base_models = set()
        for expert in [e for e in self.expert_registry.experts() if e.has_model()]:
            modelfile_contents = expert.model.modelfile_contents()
            match = re.match(r"FROM ([^\s]+).*", modelfile_contents)
            if match:
                base_models.add(match.group(1))
        return base_models

    def _get_installed_models(self):
        response = ollama.list()
        existing_model_names = [
            model["name"].split(":")[0] for model in response["models"]
        ]
        return set(existing_model_names)

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        base_models_needed = self._get_all_base_models()
        print("Base Ollama models needed: ", base_models_needed)
        installed_models = self._get_installed_models()
        for base_model in base_models_needed:
            if base_model in installed_models:
                print(f"  {base_model} already installed")
            else:
                print(f"  Pulling {base_model} from Ollama")
                stream = ollama.pull(base_model, stream=True)
                last_message = ""
                for chunk in stream:
                    current_message = chunk["status"]
                    if current_message != last_message:
                        print("    ", current_message)
                    last_message = current_message
                installed_models.add(base_model)
        self.refresh.generate(lmoe_query)
