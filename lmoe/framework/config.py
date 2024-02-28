from dataclasses import dataclass
from functools import lru_cache
from string import Template
from typing import List, Optional

import os
import toml


# The absolute path to the .lmoeconfig file located under the user's home directory.
_LMOE_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".lmoeconfig")

# The default base model to use if none is specified in a config.
_DEFAULT_BASE_OLLAMA_MODEL = "mistral"

# Default configuration if none is supplied or able to be successfully read.
_LMOE_DEFAULT_CONFIG = Template(
    """
plugins = []
[ollama]
base_ollama_model = $base_ollama_model
"""
)


def _get_default_toml():
    return toml.loads(
        _LMOE_DEFAULT_CONFIG.substitute(base_ollama_model=_DEFAULT_BASE_OLLAMA_MODEL)
    )


@dataclass(frozen=True)
class LmoePlugins:
    """A pointer to a package containing 1 or more lmoe plugin modules."""

    package_name: str
    path: str

    @classmethod
    def from_toml(cls, toml_dict) -> List["LmoePlugins"]:
        return [LmoePlugins(**d) for d in toml_dict["plugins"]]


@dataclass(frozen=True)
class OllamaConfig:
    """Various settings related to interacting with Ollama."""

    # The base Ollama model which will parent all lmoe specializations. Keeping this consistent
    # between models ensures the model remains resident in memory (different modelfiles only
    # update a few weights), so this ensures speed is high.
    base_ollama_model: str

    _BASE_OLLAMA_MODEL = "ollama.base_ollama_model"

    @classmethod
    def from_toml(cls, toml_dict) -> "OllamaConfig":
        base_ollama_model = _DEFAULT_BASE_OLLAMA_MODEL
        if cls._BASE_OLLAMA_MODEL in toml_dict:
            base_ollama_model = toml_dict[cls._BASE_OLLAMA_MODEL]
        return OllamaConfig(base_ollama_model)


@dataclass(frozen=True)
class LmoeConfig:
    """An immutable representatino of lmoe's configuration state."""

    lmoe_plugins: List[LmoePlugins]
    ollama_config: OllamaConfig

    @classmethod
    def _load_from_dict(cls, lmoe_config_dict) -> "LmoeConfig":
        return LmoeConfig(
            lmoe_plugins=LmoePlugins.from_toml(lmoe_config_dict),
            ollama_config=OllamaConfig.from_toml(lmoe_config_dict),
        )

    @classmethod
    @lru_cache
    def load(cls) -> "LmoeConfig":
        try:
            with open(_LMOE_CONFIG_FILE, "r") as f:
                return cls._load_from_dict(toml.load(f))
        except FileNotFoundError as e:
            print(
                f"No config file readable at {_LMOE_CONFIG_FILE}, using default config."
            )
            return cls._load_from_dict(_get_default_toml())
