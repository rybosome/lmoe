from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

import os
import toml


# The absolute path to the .lmoeconfig file located under the user's home directory.
_LMOE_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".lmoeconfig")

# Default configuration if none is supplied or able to be successfully read.
_LMOE_DEFAULT_CONFIG = """
plugins = []
"""


@dataclass(frozen=True)
class LmoePlugins:
    """A pointer to a package containing 1 or more lmoe plugin modules."""

    package_name: str
    path: str


@dataclass(frozen=True)
class LmoeConfig:
    """An immutable representatino of lmoe's configuration state."""

    lmoe_plugins: Optional[List[LmoePlugins]]

    @classmethod
    def _load_from_dict(cls, lmoe_config_dict) -> "LmoeConfig":
        lmoe_plugins = [LmoePlugins(**d) for d in lmoe_config_dict["plugins"]]
        return LmoeConfig(lmoe_plugins=lmoe_plugins)

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
            return cls._load_from_dict(toml.loads(_LMOE_DEFAULT_CONFIG))
