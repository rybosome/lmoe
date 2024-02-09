from lmoe.api.lmoe_query import LmoeQuery
from abc import ABC, abstractmethod

import argparse


class Command(ABC):

    @abstractmethod
    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        pass
