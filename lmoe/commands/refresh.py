import argparse

from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.framework.model_registry import ModelRegistry


@inject
@dataclass
class Refresh(Command):

    model_registry: ModelRegistry

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        print("Refreshing Ollama's models: ", self.model_registry.lmoe_model_names())
        self.model_registry.refresh()
