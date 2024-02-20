import pytest

from lmoe.framework.module_loader import load_native_and_plugin_modules


@pytest.fixture(scope="module")
def real_injector():
    """Returns the real injector used by the execution path.

    Module-scoped, so only instantiated once per test file.
    """
    yield load_native_and_plugin_modules()
