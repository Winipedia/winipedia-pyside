"""Workflow configs."""

from typing import Any

from winipedia_utils.git.github.workflows.base.base import Workflow as WinipediaWorkflow
from winipedia_utils.git.github.workflows.health_check import (
    HealthCheckWorkflow as WinipediaHealthCheckWorkflow,
)
from winipedia_utils.git.github.workflows.release import (
    ReleaseWorkflow as WinipediaReleaseWorkflow,
)


class PySide6WorkflowMixin(WinipediaWorkflow):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    @classmethod
    def get_pre_commit_step(cls) -> dict[str, Any]:
        """Get the pre-commit step.

        We need to add some env vars
        so QtWebEngine doesn't try to use GPU acceleration etc.
        """
        step = super().get_pre_commit_step()
        step["env"] = {
            "QT_QPA_PLATFORM": "offscreen",
            "QTWEBENGINE_DISABLE_SANDBOX": "1",
            "QTWEBENGINE_CHROMIUM_FLAGS": "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage",  # noqa: E501
        }
        return step

    @classmethod
    def get_poetry_setup_steps(
        cls,
        *args: Any,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Get the poetry setup steps.

        We need to install additional system dependencies for pyside6.
        """
        steps = super().get_poetry_setup_steps(
            *args,
            **kwargs,
        )
        steps.append(
            {
                "name": "Install PySide6 System Dependencies",
                "run": "sudo apt-get update && sudo apt-get install -y libegl1 libpulse0",  # noqa: E501
            }
        )
        return steps


class HealthCheckWorkflow(PySide6WorkflowMixin, WinipediaHealthCheckWorkflow):
    """Health check workflow.

    Extends winipedia_utils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflow(PySide6WorkflowMixin, WinipediaReleaseWorkflow):
    """Release workflow.

    Extends winipedia_utils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """
