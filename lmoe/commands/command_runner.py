from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.initialize import Initialize
from lmoe.commands.print_classification import PrintClassification
from lmoe.commands.print_classifier_modelfile import PrintClassifierModelfile
from lmoe.commands.query import Query
from lmoe.commands.refresh import Refresh
from lmoe.commands.version import Version

import argparse


@inject
@dataclass
class CommandRunner:

    parsed_args: argparse.Namespace
    lmoe_query: LmoeQuery
    initialize: Initialize
    print_classification: PrintClassification
    print_classifier_modelfile: PrintClassifierModelfile
    query: Query
    refresh: Refresh
    version: Version

    def execute(self):
        command = None

        if self.parsed_args.classify:
            command = self.print_classification
        elif self.parsed_args.classifier_modelfile:
            command = self.print_classifier_modelfile
        elif self.parsed_args.refresh:
            command = self.refresh
        elif self.parsed_args.version:
            command = self.version
        elif self.parsed_args.initialize:
            command = self.initialize
        else:
            command = self.query

        command.execute(self.parsed_args, self.lmoe_query)
