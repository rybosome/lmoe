import argparse
import contextlib
import io

from lmoe.api.lmoe_query import LmoeQuery
from lmoe.commands.version import Version
from lmoe.definitions import get_project_version


class TestVersion:

    def test_print_version(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            Version().execute(
                argparse.Namespace(),
                LmoeQuery(stdin_context="", paste_context="", user_query=""),
            )
        assert f"{get_project_version()}" in f.getvalue()
