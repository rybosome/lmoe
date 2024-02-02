from lmoe.experts import classifier

import argparse
import pyperclip
import sys


def run():
    parser = argparse.ArgumentParser(
        description="Provide optional context for a query to lmoe through STDIN or the clipboard, then ask a question about it."
    )
    parser.add_argument("query", nargs="+", default=None, help="Query for lmoe")
    parser.add_argument(
        "--paste", action="store_true", help="Read content from the clipboard."
    )
    parser.add_argument(
        "--classify",
        action="store_true",
        help="Classify a query, determine which expert should respond to the query without actually responding.",
    )

    args = parser.parse_args()

    user_query = " ".join(args.query)

    if args.classify:
        classify(user_query)
    else:
        user_context = ""

        # Check if there is context on STDIN or the clipboard
        if not sys.stdin.isatty():
            user_context = sys.stdin.read()
        elif args.paste:
            if clipboard_content := pyperclip.paste():
                user_context = clipboard_content

        query(user_context, user_query)


def query(user_context, user_query):
    expert = classifier.classify(user_query)
    expert.generate(user_context, user_query)


def classify(user_query):
    expert = classifier.classify(user_query)
    print(expert.expert_type())
    print("")
