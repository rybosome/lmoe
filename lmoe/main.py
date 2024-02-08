from lmoe.api.lmoe_query import LmoeQuery
from lmoe.experts.classifier import Classifier
from lmoe.experts.refresh import Refresh
from lmoe.framework import expert_registry
from typing import Optional

import argparse
import pyperclip
import sys


def run():
    parser = argparse.ArgumentParser(
        description="Provide optional context for a query to lmoe through STDIN or the clipboard, then ask a question about it."
    )
    parser.add_argument("query", nargs="*", default=None, help="Query for lmoe. Use natural language.")

    parser.add_argument(
        "--paste", action="store_true", help="Add context to your query from the system clipboard."
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

    args = parser.parse_args()

    user_query = " ".join(args.query)
    classifier = expert_registry.get_expert(Classifier.name())

    ## Debug options

    ##
    ## Classify a query, print the expert which would respond to it.
    if args.classify:
        target_expert = classifier.classify(user_query)
        print(target_expert.name())
        print("")
        exit(0)

    ##
    ## Print the contents of the classifier modelfile. Used to bootstrap lmoe.
    if args.classifier_modelfile:
        print(classifier.modelfile_contents())
        exit(0)

    ##
    ## Refreshes the modelfiles with Ollama.
    if args.refresh:
        expert_registry.get_expert(Refresh.name()).generate("", "")
        exit(0)

    stdin_context: Optional[str] = None
    if not sys.stdin.isatty():
        stdin_context = sys.stdin.read()

    paste_context: Optional[str] = None
    if args.paste:
        if clipboard_content := pyperclip.paste():
            paste_context = clipboard_content

    target_expert = classifier.classify(user_query)
    target_expert.generate(LmoeQuery(stdin_context, paste_context, user_query))
