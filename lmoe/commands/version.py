from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.definitions import get_project_version

import argparse


class Version(Command):

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        print(get_project_version())
