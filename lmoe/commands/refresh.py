from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.experts.refresh import Refresh

import argparse


class Refresh(Command):

    @inject
    def __init__(self, refresh: Refresh):
        self.refresh = refresh

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        self.refresh.generate(lmoe_query)
