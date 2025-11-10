"""Tests for winipedia_pyside.ui.pages.browser module."""

from PySide6.QtWidgets import QVBoxLayout
from pytest_mock import MockerFixture
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg

from winipedia_pyside.utils.ui.pages import browser
from winipedia_pyside.utils.ui.pages.browser import Browser


class TestBrowser:
    """Test class for Browser."""

    def test_setup(self, mocker: MockerFixture) -> None:
        """Test method for setup."""
        # Mock the Browser class methods to avoid abstract class issues
        mock_add_brwoser = mocker.patch.object(Browser, "add_brwoser")

        # Create a mock instance
        mock_browser = mocker.MagicMock(spec=Browser)
        mock_browser.add_brwoser = mock_add_brwoser

        # Call setup method directly on the class
        Browser.setup(mock_browser)

        # Verify add_brwoser was called
        mock_add_brwoser.assert_called_once()
        assert_with_msg(mock_add_brwoser.called, "setup should call add_brwoser method")

        # Test that setup method exists and is final
        assert_with_msg(hasattr(Browser, "setup"), "Browser should have setup method")
        assert_with_msg(callable(Browser.setup), "setup should be callable")

    def test_add_brwoser(self, mocker: MockerFixture) -> None:
        """Test method for add_brwoser."""
        # Mock the BrowserWidget class
        mock_browser_widget_class = mocker.patch(
            make_obj_importpath(browser) + ".BrowserWidget"
        )
        mock_browser_widget_instance = mocker.MagicMock()
        mock_browser_widget_class.return_value = mock_browser_widget_instance

        # Create a mock browser instance with v_layout
        mock_browser = mocker.MagicMock(spec=Browser)
        mock_layout = mocker.MagicMock(spec=QVBoxLayout)
        mock_browser.v_layout = mock_layout

        # Call add_brwoser method directly on the class
        Browser.add_brwoser(mock_browser)

        # Verify BrowserWidget was instantiated with correct layout
        mock_browser_widget_class.assert_called_once_with(mock_layout)

        # Verify the browser widget was assigned to the browser attribute
        assert_with_msg(
            mock_browser.browser is mock_browser_widget_instance,
            "add_brwoser should assign BrowserWidget instance to browser attribute",
        )

        # Test that the method exists and is final
        assert_with_msg(
            hasattr(Browser, "add_brwoser"), "Browser should have add_brwoser method"
        )
        assert_with_msg(callable(Browser.add_brwoser), "add_brwoser should be callable")

        # Test that it's a method of the Browser class
        assert_with_msg(
            "add_brwoser" in Browser.__dict__,
            "add_brwoser should be defined in Browser class",
        )
