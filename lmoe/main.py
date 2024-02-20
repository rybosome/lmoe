from injector import Injector
from lmoe.commands.command_runner import CommandRunner
from lmoe.framework.config import LmoeConfig
from lmoe.framework.native_module import NativeModule
from lmoe.framework.plugin_module_registry import PluginModuleRegistry
from lmoe.framework.module_loader import load_native_and_plugin_modules

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

    injector = load_native_and_plugin_modules()

    # Defer execution to the command runner
    command_runner = injector.get(CommandRunner)
    command_runner.execute()
