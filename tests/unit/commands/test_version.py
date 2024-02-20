import argparse

from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.version import Version
from lmoe.definitions import get_project_version
from tests.util.capture_output import capture_console_output
from tests.util.real_injector import real_injector


class TestVersion:

    def test_print_version(self, real_injector):
        with capture_console_output() as console_output:
            real_injector.get(Version).execute(argparse.Namespace(), LmoeQuery.empty())
            assert f"{get_project_version()}" in console_output.getvalue()
