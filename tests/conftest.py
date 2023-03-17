import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--connected", action="store_true", default=False, help="run connected tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "screen: mark test as connected to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--connected"):
        # --connected given in cli: do not skip slow tests
        return
    skip_screen = pytest.mark.skip(reason="need --connected option to run")
    for item in items:
        if "screen" in item.keywords:
            item.add_marker(skip_screen)
