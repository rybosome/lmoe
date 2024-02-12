from abc import ABC, abstractmethod
from lmoe.api.model import Model
from lmoe.utils.templates import read_template
from typing import List, Optional


class BaseExpert(ABC):

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """The unique name of this capability."""
        pass

    @classmethod
    @abstractmethod
    def has_model(cls) -> bool:
        """Whether or not this capability is backed by a model."""
        pass

    @abstractmethod
    def description(self) -> str:
        """A one-line description of this capability, used as input to the root classifier."""
        pass

    @abstractmethod
    def example_queries(self) -> List[str]:
        """A list of queries which should be routed to this capability."""
        pass
