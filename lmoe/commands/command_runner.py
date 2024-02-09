from lmoe.commands.print_classification import PrintClassification
from lmoe.commands.print_classifier_modelfile import PrintClassifierModelfile
from lmoe.commands.query import Query
from lmoe.commands.refresh import Refresh
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery

import argparse


class CommandRunner:

    @inject
    def __init__(
        self,
        parsed_args: argparse.Namespace,
        lmoe_query: LmoeQuery,
        print_classification: PrintClassification,
        print_classifier_modelfile: PrintClassifierModelfile,
        query: Query,
        refresh: Refresh,
    ):
        self.parsed_args = parsed_args
        self.lmoe_query = lmoe_query
        self.print_classification = print_classification
        self.print_classifier_modelfile = print_classifier_modelfile
        self.query = query
        self.refresh = refresh

    def execute(self):
        command = None

        if self.parsed_args.classify:
            command = self.print_classification
        elif self.parsed_args.classifier_modelfile:
            command = self.print_classifier_modelfile
        elif self.parsed_args.refresh:
            command = self.refresh
        else:
            command = self.query

        command.execute(self.parsed_args, self.lmoe_query)
