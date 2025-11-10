"""module."""

from winipedia_utils.utils.testing.assertions import assert_with_msg

from winipedia_pyside.dev.configs.configs import HealthCheckWorkflow, ReleaseWorkflow


class TestPySideWorkflowMixin:
    """Test class for PySide6WorkflowMixin."""

    def test_step_run_pre_commit_hooks(self) -> None:
        """Test method for step_run_pre_commit_hooks."""
        step = HealthCheckWorkflow.step_run_pre_commit_hooks()
        assert_with_msg("env" in step, "Step should have env vars")
        assert_with_msg(
            step["env"]["QT_QPA_PLATFORM"] == "offscreen",
            "QT_QPA_PLATFORM should be offscreen",
        )

    def test_steps_core_matrix_setup(self) -> None:
        """Test method for steps_core_matrix_setup."""
        steps = HealthCheckWorkflow.steps_core_matrix_setup()
        assert_with_msg(isinstance(steps, list), "Steps should be a list")

    def test_step_install_pyside_system_dependencies(self) -> None:
        """Test method for step_install_pyside_system_dependencies."""
        step = HealthCheckWorkflow.step_install_pyside_system_dependencies()
        assert_with_msg("run" in step, "Step should have run command")


class TestHealthCheckWorkflow:
    """Test class for HealthCheckWorkflow."""


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""

    def test_steps_release(self) -> None:
        """Test method for steps_release."""
        steps = ReleaseWorkflow.steps_release()
        assert_with_msg(isinstance(steps, list), "Steps should be a list")
