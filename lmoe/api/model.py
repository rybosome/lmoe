from dataclasses import dataclass
from lmoe.definitions import get_project_version
from lmoe.utils.templates import read_template
from typing import Optional


@dataclass
class Model:
    """A basic Ollama model with a tuned modelfile.

    The modelfile is located in the templates directory at {name}.modelfile.txt and contains no
    additional templating such as examples, descriptions, etc.
    """

    name: str
    """The name of the model."""

    def ollama_name(self) -> str:
        """The name of this model in Ollama, a string which includes a namespace prefix and version."""
        return f"lmoe_{self.name.lower()}_{get_project_version()}"

    def modelfile_name(self) -> str:
        """The filename (without a path) of the backing Ollama model.

        `lmoe` convention is to use the model name suffixed with '.modelfile.txt':
          * code.modelfile.txt
          * general.modelfile.txt
          * etc.
        """
        return f"{self.name.lower()}.modelfile.txt"

    def modelfile_contents(self) -> Optional[str]:
        """The contents of the modelfile.

        May be overridden for dynamically generated modelfiles."""
        return read_template(self.modelfile_name())
