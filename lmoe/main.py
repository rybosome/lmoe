from lmoe.experts.classifier import Classifier
from lmoe.experts.refresh import Refresh
from lmoe.framework import expert_registry

import argparse
import pyperclip
import sys


def run():
    parser = argparse.ArgumentParser(
        description="Provide optional context for a query to lmoe through STDIN or the clipboard, then ask a question about it."
    )
    parser.add_argument("query", nargs="*", default=None, help="Query for lmoe")
    parser.add_argument(
        "--paste", action="store_true", help="Read content from the clipboard."
    )
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

    if args.classify:
        target_expert = classifier.classify(user_query)
        print(target_expert.name())
        print("")
    elif args.classifier_modelfile:
        print(classifier.modelfile_contents())
    elif args.refresh:
        expert_registry.get_expert(Refresh.name()).generate("", "")
    else:
        print("")
        user_context = ""
        target_expert = classifier.classify(user_query)

        # Check if there is context on STDIN or the clipboard
        if not sys.stdin.isatty():
            user_context = sys.stdin.read()
        elif args.paste:
            if clipboard_content := pyperclip.paste():
                user_context = clipboard_content

        target_expert.generate(user_context, user_query)
