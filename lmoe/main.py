from injector import Injector
from lmoe.commands.command_runner import CommandRunner
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
    # Dynamically import native experts
    native_path = os.path.dirname(lmoe.experts.__file__)
    import_experts(native_path)

    # Dynamically import plugin experts
    # TODO: support for configuring the plugin directory, naming, etc.
    home_directory = os.path.expanduser("~")

    # Add the parent plugin directory to the Python path
    plugin_parent_path = f"{home_directory}/lmoe_plugins"
    sys.path.append(plugin_parent_path)

    # Import the plugin Python module
    plugin_path = f"{plugin_parent_path}/lmoe_plugins"
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
