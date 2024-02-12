from injector import inject
from lmoe.api.base_expert import BaseExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert
from typing import List

import argparse


# @expert
class PrintArgs(BaseExpert):

    def __init__(self, parsed_args: argparse.Namespace):
        self.parsed_args = parsed_args

    @classmethod
    def name(cls) -> str:
        return "PRINT_ARGS"

    @classmethod
    def has_model(cls) -> bool:
        return False

    def description(self) -> str:
        return "Prints the commandline arguments that were used to invoke lmoe."

    def example_queries(self) -> List[str]:
        return [
            "print args",
            "print the commandline args",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        print("These are the arguments that were passed to me:")
        print(self.parsed_args)
