from injector import Injector, inject
from typing import List


def expert(cls):
    """Decorator to register an Expert with the ExpertRegistry."""
    ExpertRegistry.register(cls)
    return cls


class ExpertRegistry:
    """A registry of all of the individual experts within lmoe.

    Experts are keyed on their name, which allows the default experts to be overridden with
    user-defined experts.
    """

    _expert_registry = {}

    @inject
    def __init__(self, injector: Injector):
        self.injector = injector

    @classmethod
    def register(cls, *args) -> None:
        """Register one or more experts - does not instantiate them."""
        for expert_type in args:
            cls._expert_registry[expert_type.name()] = expert_type

    @classmethod
    def names(cls) -> List[str]:
        """List of experts which have been registered."""
        return [key for key in cls._expert_registry.keys()]

    @classmethod
    def modelfile_names(cls) -> List[str]:
        """List of known modelfiles backed by registered experts."""
        return [
            expert_type.modelfile_name()
            for expert_type in cls._expert_registry.values()
            if expert_type.has_modelfile()
        ]

    def experts(self):
        return [self.get(expert_name) for expert_name in ExpertRegistry.names()]

    def get(self, expert_name):
        if expert_name not in self._expert_registry:
            return None
        expert_type = self._expert_registry[expert_name]
        return self.injector.get(expert_type)
