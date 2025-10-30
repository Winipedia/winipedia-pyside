"""Pytest configuration for tests.

This module configures pytest plugins for the test suite, setting up the necessary
fixtures and hooks for the different
test scopes (function, class, module, package, session).
It also import custom plugins from tests/base/scopes.
This file should not be modified manually.
"""

pytest_plugins = ["winipedia_utils.testing.tests.conftest"]

import pytest
from winipedia_utils.git.github.github import running_in_github_actions

if running_in_github_actions():
    pytest.skip("Skipping tests in GitHub Actions")
