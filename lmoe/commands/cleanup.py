import argparse
import re
import semantic_version

from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.definitions import get_project_version
from lmoe.framework.model_registry import ModelRegistry
from lmoe.framework.ollama_client import OllamaClient
from semantic_version import Version

from typing import Optional


def parse_version(model_name: str) -> Optional[Version]:
    # Modern lmoe naming scheme
    match = re.match("lmoe.*?:([0-9]+\.[0-9]+\.[0-9]+.*)", model_name)
    if match:
        return Version(match.group(1))

    legacy_match = re.match("lmoe_.*?_([0-9]+\.[0-9]+\.[0-9]+):latest", model_name)
    if legacy_match:
        return Version(legacy_match.group(1))

    return None


@inject
@dataclass
class Cleanup(Command):

    model_registry: ModelRegistry
    ollama_client: OllamaClient

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        current_version = get_project_version()

        installed_models = self.model_registry.installed_ollama_model_names()
        lmoe_models = [m for m in installed_models if m.startswith("lmoe")]
        models_to_delete = [
            m
            for m in lmoe_models
            if (parsed_version := parse_version(m)) and parsed_version < current_version
        ]

        if not models_to_delete:
            print("Already cleaned up")
            exit(0)

        print(f"Deleting these models:\n", models_to_delete)
        confirmation = input("Proceed? (y/n): ")
        if confirmation == "y":
            for m in models_to_delete:
                print(f"Deleting {m}")
                self.ollama_client.delete_ollama_model(m)
