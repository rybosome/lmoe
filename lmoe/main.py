from injector import Injector
from lmoe.commands.command_runner import CommandRunner
from lmoe.framework.module_loader import load_native_and_plugin_modules


def run():
    injector = load_native_and_plugin_modules()

    # Defer execution to the command runner
    command_runner = injector.get(CommandRunner)
    command_runner.execute()
