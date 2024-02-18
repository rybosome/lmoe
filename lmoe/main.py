from injector import Injector
from lmoe.commands.command_runner import CommandRunner
from lmoe.framework.config import LmoeConfig
from lmoe.framework.native_module import NativeModule
from lmoe.framework.plugin_module_registry import PluginModuleRegistry

import importlib.util
import lmoe.experts
import os
import pkgutil
import sys


def import_experts(package_path):
    for file_name in os.listdir(package_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = file_name[:-3]  # Remove '.py' extension
            module_path = os.path.join(package_path, file_name)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)


def run():
    # Load lmoe config
    lmoe_config = LmoeConfig.load()

    # Dynamically import native experts
    native_path = os.path.dirname(lmoe.experts.__file__)
    import_experts(native_path)

    # Dynamically import plugin experts, paths are defined in $HOME/.lmoeconfig
    for lmoe_plugins in lmoe_config.lmoe_plugins or []:
        # Add the parent plugin directory to the Python path
        sys.path.append(lmoe_plugins.path)
        plugin_path = os.path.join(lmoe_plugins.path, lmoe_plugins.package_name)

        # Import the plugin Python modules
        try:
            import_experts(plugin_path)
        except FileNotFoundError as e:
            # Ignore for now, only notify that no plugins were loaded.
            print(f"No plugins loaded from {plugin_path}")

    # Carry on with app instantiation, install native and plugin injection modules
    modules = [NativeModule]
    modules.extend(PluginModuleRegistry.modules())
    injector = Injector(modules)

    # Defer execution to the command runner
    command_runner = injector.get(CommandRunner)
    command_runner.execute()
