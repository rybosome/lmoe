import contextlib
import io
import sys


@contextlib.contextmanager
def capture_console_output():
    """Creates a managed string buffer which captures console output, used for testing.

    Example:
    with capture_console_output() as console_output():
        DoSomethingWhichPrintsToTheConsole()
        assert "values expected to be printed to stdout" in console_output.getvalue()
    """
    # Create a StringIO object to capture the console output
    console_output = io.StringIO()

    # Redirect stdout to the StringIO object
    sys.stdout = console_output
    try:
        yield console_output
    finally:
        # Restore the original stdout
        sys.stdout = sys.__stdout__
