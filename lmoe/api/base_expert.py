from abc import ABC, abstractmethod
from collections.abc import Sequence
from lmoe.utils.templates import read_template
from typing import Optional


class BaseExpert(ABC):
    """Base class for any lmoe capability.

    Capabilities may or may not be backed by a model.
    """

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """The unique name of this capability."""
        pass

    @classmethod
    @abstractmethod
    def has_modelfile(cls) -> bool:
        """Whether or not this capability is backed by a model."""
        pass

    @classmethod
    def model_name(cls) -> Optional[str]:
        """The name of the Ollama model, if this is model-backed.

        lmoe_code
        lmoe_general
        etc.
        """
        return f"lmoe_{cls.name().lower()}" if cls.has_modelfile else None

    @classmethod
    def modelfile_name(cls) -> Optional[str]:
        """The filename (without a path) of the backing Ollama model, if this is model-backed.

        code.modelfile.txt
        general.modelfile.txt
        """
        return f"{cls.name().lower()}.modelfile.txt" if cls.has_modelfile else None

    @abstractmethod
    def description(self) -> str:
        """A one-line description of this capability, used as input to the root classifier."""
        pass

    @abstractmethod
    def examples(self) -> Sequence[str]:
        """A list of queries which should be routed to this capability."""
        pass

    def modelfile_contents(self) -> Optional[str]:
        """The contents of the modelfile, if this is model-backed - may be overridden for dynamically generated modelfiles."""
        return read_template(self.modelfile_name()) if self.has_modelfile else None
