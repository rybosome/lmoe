from injector import Module, provider, singleton
from lmoe.framework.plugin_module_registry import plugin_module
from lmoe_plugins.print_args import PrintArgs

import argparse


# @plugin_module
class LmoePluginModule(Module):

    @singleton
    @provider
    def provide_print_args(self, parsed_args: argparse.Namespace) -> PrintArgs:
        return PrintArgs(parsed_args)
