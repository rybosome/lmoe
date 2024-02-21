import argparse

from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.framework.ollama_client import OllamaClient


@inject
@dataclass
class Passthrough(Command):

    ollama_client: OllamaClient

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        self.ollama_client.stream_raw(
            model_name=parsed_args.passthrough, prompt=lmoe_query.user_query
        )
