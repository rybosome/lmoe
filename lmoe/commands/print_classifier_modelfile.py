from lmoe.commands.command import Command
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.experts.classifier import Classifier

import argparse


class PrintClassifierModelfile(Command):

    @inject
    def __init__(self, classifier: Classifier):
        self.classifier = classifier

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        print(self.classifier.modelfile_contents())
