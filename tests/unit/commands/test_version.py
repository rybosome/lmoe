import argparse

from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.version import Version
from lmoe.definitions import get_project_version
from tests.util.capture_output import capture_console_output


class TestVersion:

    def test_print_version_capture_console_output(self):
        with capture_console_output() as console_output:
            Version().execute(argparse.Namespace(), LmoeQuery.empty())
            assert f"{get_project_version()}" in console_output.getvalue()
