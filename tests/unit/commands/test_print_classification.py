import argparse
import pytest

from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.print_classification import PrintClassification
from tests.util.capture_output import capture_console_output
from tests.util.real_injector import real_injector


@pytest.fixture
def test_cmd(real_injector):
    yield real_injector.get(PrintClassification)


class TestPrintClassifierModelfile:

    def _assert_classification(
        self, test_cmd: PrintClassification, query: str, classification: str
    ):
        with capture_console_output() as console_output:
            test_cmd.execute(
                argparse.Namespace(),
                LmoeQuery(stdin_context=None, paste_context=None, user_query=query),
            )
            assert classification in console_output.getvalue()

    def test_general(self, test_cmd: PrintClassification):
        self._assert_classification(test_cmd, "what is the ionosphere", "GENERAL")

    def test_random_weather_plugin(self, test_cmd: PrintClassification):
        self._assert_classification(test_cmd, "random weather", "RANDOM_WEATHER")
