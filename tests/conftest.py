"""Pytest configuration."""

from pathlib import Path

import pytest

# we decided to use the pytest plugin from sphinx itself to access the sphinx test utilities
# the only requirement is to set the rootdir inside your conftest.py file
# in this demo case the test documentation are stored in a "roots" folder
pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    """Get the root directory for the whole test session."""
    return Path(__file__).parent.resolve() / "roots"
