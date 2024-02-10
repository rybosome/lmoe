from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.experts.classifier import Classifier

import argparse


@inject
@dataclass
class PrintClassification(Command):

    classifier: Classifier

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        print(self.classifier.classify(lmoe_query))
