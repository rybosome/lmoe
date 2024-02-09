from lmoe.commands.command import Command
from injector import inject
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.experts.classifier import Classifier
from lmoe.framework.expert_registry import ExpertRegistry

import argparse


class Query(Command):

    @inject
    def __init__(self, classifier: Classifier, expert_registry: ExpertRegistry):
        self.classifier = classifier
        self.expert_registry = expert_registry

    def execute(self, parsed_args: argparse.Namespace, lmoe_query: LmoeQuery) -> None:
        target_expert_name = self.classifier.classify(lmoe_query.user_query)
        target_expert = self.expert_registry.get(target_expert_name)
        target_expert.generate(lmoe_query)
