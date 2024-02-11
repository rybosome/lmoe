from injector import Module, provider, singleton
from lmoe.api.lmoe_query import LmoeQuery
from typing import Optional

import argparse
import pyperclip
import sys


class NativeModule(Module):

    @singleton
    @provider
    def provide_parsed_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Provide optional context for a query to lmoe through STDIN or the clipboard, then ask a question about it."
        )
        parser.add_argument(
            "query",
            nargs="*",
            default=None,
            help="Query for lmoe. Use natural language.",
        )

        ## Behavior flags
        parser.add_argument(
            "--paste",
            action="store_true",
            help="Add context to your query from the system clipboard.",
        )
        parser.add_argument(
            "--initialize",
            action="store_true",
            help="Initialize a new installation of lmoe.",
        )
        parser.add_argument(
            "--version", action="store_true", help="Print the current version string."
        )

        ## Debug flags
        parser.add_argument(
            "--classify",
            action="store_true",
            help="Classify a query, determine which expert should respond to the query without actually responding.",
        )
        parser.add_argument(
            "--classifier_modelfile",
            action="store_true",
            help="Print the classifier modelfile.",
        )
        parser.add_argument(
            "--refresh", action="store_true", help="Force a modelfile refresh."
        )

        return parser.parse_args()

    @singleton
    @provider
    def provide_lmoe_query(self, parsed_args: argparse.Namespace) -> LmoeQuery:
        stdin_context: Optional[str] = None
        if not sys.stdin.isatty():
            stdin_context = sys.stdin.read()

        paste_context: Optional[str] = None
        if parsed_args.paste:
            if clipboard_content := pyperclip.paste():
                paste_context = clipboard_content
        return LmoeQuery(stdin_context, paste_context, " ".join(parsed_args.query))
