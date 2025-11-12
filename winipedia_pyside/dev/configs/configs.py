"""Configs for winipedia_utils.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from typing import Any

from winipedia_utils.dev.configs.workflows.base.base import (
    Workflow as WinipediaWorkflow,
)
from winipedia_utils.dev.configs.workflows.health_check import (
    HealthCheckWorkflow as WinipediaHealthCheckWorkflow,
)
from winipedia_utils.dev.configs.workflows.release import (
    ReleaseWorkflow as WinipediaReleaseWorkflow,
)


class PySideWorkflowMixin(WinipediaWorkflow):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    @classmethod
    def step_run_tests(
        cls,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Get the pre-commit step.

        We need to add some env vars
        so QtWebEngine doesn't try to use GPU acceleration etc.
        """
        step = super().step_run_tests(step=step)
        step.setdefault("env", {}).update(
            {
                "QT_QPA_PLATFORM": "offscreen",
                "QTWEBENGINE_DISABLE_SANDBOX": "1",
                "QTWEBENGINE_CHROMIUM_FLAGS": "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage",  # noqa: E501
            }
        )
        return step

    @classmethod
    def steps_core_matrix_setup(
        cls, python_version: str | None = None, *, repo_token: bool = False
    ) -> list[dict[str, Any]]:
        """Get the poetry setup steps.

        We need to install additional system dependencies for pyside6.
        """
        steps = super().steps_core_matrix_setup(python_version, repo_token=repo_token)

        steps.append(
            cls.step_install_pyside_system_dependencies(),
        )
        return steps

    @classmethod
    def step_install_pyside_system_dependencies(cls) -> dict[str, Any]:
        """Get the step to install PySide6 dependencies."""
        return cls.get_step(
            step_func=cls.step_install_pyside_system_dependencies,
            run="sudo apt-get update && sudo apt-get install -y libegl1 libpulse0",
            if_condition="runner.os == 'Linux'",
        )


class HealthCheckWorkflow(PySideWorkflowMixin, WinipediaHealthCheckWorkflow):
    """Health check workflow.

    Extends winipedia_utils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflow(HealthCheckWorkflow, WinipediaReleaseWorkflow):
    """Release workflow.

    Extends winipedia_utils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """

    @classmethod
    def steps_release(cls) -> list[dict[str, Any]]:
        """Get the release steps."""
        steps = super().steps_release()
        # find the index of the cls.step_install_python_dependencies step and insert
        # the pyside6 dependencies step after it
        index = (
            next(
                i
                for i, step in enumerate(steps)
                if step["id"]
                == cls.make_id_from_func(cls.step_install_python_dependencies)
            )
            + 1
        )
        steps.insert(index, cls.step_install_pyside_system_dependencies())
        return steps
