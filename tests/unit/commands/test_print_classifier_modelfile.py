import argparse

from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.print_classifier_modelfile import PrintClassifierModelfile
from tests.util.capture_output import capture_console_output
from tests.util.real_injector import real_injector


class TestPrintClassifierModelfile:

    def test_print_classifier_modelfile(self, real_injector):
        with capture_console_output() as console_output:
            real_injector.get(PrintClassifierModelfile).execute(
                argparse.Namespace(), LmoeQuery.empty()
            )
            assert (
                "It is your job to classify a user's query" in console_output.getvalue()
            )
