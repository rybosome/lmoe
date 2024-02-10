from dataclasses import dataclass
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.command import Command
from lmoe.experts.classifier import Classifier
from lmoe.framework.expert_registry import ExpertRegistry

import argparse


@inject
@dataclass
class Query(Command):

    classifier: Classifier
    expert_registry: ExpertRegistry

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        target_expert_name = self.classifier.classify(lmoe_query.user_query)
        target_expert = self.expert_registry.get(target_expert_name)
        target_expert.generate(lmoe_query)
