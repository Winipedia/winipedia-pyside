"""module."""

import pytest
from winipedia_utils.git.github.github import running_in_github_actions
from winipedia_utils.testing.fixtures import autouse_session_fixture


@autouse_session_fixture
def skip_tests_in_github_actions() -> None:
    """Skip tests in GitHub Actions.

    Returns:
        bool: True if tests should be skipped, False otherwise.
    """
    if not running_in_github_actions():
        pytest.skip("Skipping tests in GitHub Actions")
