"""Tests for Base page class."""

from typing import final

from pytest_mock import MockFixture
from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.ui.pages.base.base import Base


class TestBase:
    """Test class for Base."""

    def test___init__(self, mocker: MockFixture) -> None:
        """Test method for __init__."""
        # Mock Qt components to avoid creating real widgets
        mocker.patch("PySide6.QtWidgets.QWidget.__init__")

        # Create test page class
        class TestPage(Base):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock the base_setup and other setup methods to avoid Qt operations
        mock_base_setup = mocker.patch.object(TestPage, "base_setup")
        mock_pre_setup = mocker.patch.object(TestPage, "pre_setup")
        mock_setup = mocker.patch.object(TestPage, "setup")
        mock_post_setup = mocker.patch.object(TestPage, "post_setup")

        # Create mock base window
        mock_base_window = mocker.MagicMock()

        # Test initialization
        page = TestPage(base_window=mock_base_window)

        # Verify base_window is set
        assert_with_msg(
            page.base_window is mock_base_window,
            "__init__ should set base_window attribute",
        )

        # Verify all setup methods were called in correct order
        mock_base_setup.assert_called_once()
        mock_pre_setup.assert_called_once()
        mock_setup.assert_called_once()
        mock_post_setup.assert_called_once()

    def test_base_setup(self, mocker: MockFixture) -> None:
        """Test method for base_setup."""
        # Mock Qt components to avoid creating real widgets
        mock_qvboxlayout = mocker.patch(
            "winipedia_pyside.ui.pages.base.base.QVBoxLayout"
        )
        mock_qhboxlayout = mocker.patch(
            "winipedia_pyside.ui.pages.base.base.QHBoxLayout"
        )

        # Create test page class
        class TestPage(Base):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock methods to avoid Qt operations
        mock_set_layout = mocker.patch.object(TestPage, "setLayout")
        mock_add_menu = mocker.patch.object(TestPage, "add_menu_dropdown_button")

        # Create mock base window
        mock_base_window = mocker.MagicMock()

        # Create page instance
        page = TestPage.__new__(TestPage)
        page.base_window = mock_base_window
        page.base_setup()

        # Verify Qt components were created and configured
        mock_qvboxlayout.assert_called_once()
        mock_qhboxlayout.assert_called_once()
        mock_set_layout.assert_called_once()
        mock_add_menu.assert_called_once()

        # Verify base_window.add_page was called
        mock_base_window.add_page.assert_called_once_with(page)

        # Verify layouts are set as attributes
        assert_with_msg(hasattr(page, "v_layout"), "Should create v_layout attribute")
        assert_with_msg(hasattr(page, "h_layout"), "Should create h_layout attribute")

    def test_add_menu_dropdown_button(self, mocker: MockFixture) -> None:
        """Test method for add_menu_dropdown_button."""
        # Mock Qt components
        mock_qpushbutton = mocker.patch(
            "winipedia_pyside.ui.pages.base.base.QPushButton"
        )
        mock_qmenu = mocker.patch("winipedia_pyside.ui.pages.base.base.QMenu")

        # Create test page class
        class TestPage(Base):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock dependencies
        mock_get_svg_icon = mocker.patch.object(TestPage, "get_svg_icon")
        mock_base_window = mocker.MagicMock()
        mock_base_window.get_all_page_classes.return_value = []
        mock_h_layout = mocker.MagicMock()

        # Create page instance
        page = TestPage.__new__(TestPage)
        page.base_window = mock_base_window
        page.h_layout = mock_h_layout

        page.add_menu_dropdown_button()

        # Verify components were created
        mock_qpushbutton.assert_called_once_with("Menu")
        mock_qmenu.assert_called_once()
        mock_get_svg_icon.assert_called_once_with("menu_icon")
        mock_base_window.get_all_page_classes.assert_called_once()

    def test_add_to_page_button(self, mocker: MockFixture) -> None:
        """Test method for add_to_page_button."""
        # Mock Qt components
        mock_qpushbutton = mocker.patch(
            "winipedia_pyside.ui.pages.base.base.QPushButton"
        )
        mock_button_instance = mocker.MagicMock()
        mock_qpushbutton.return_value = mock_button_instance

        # Create test page classes
        class TestPage(Base):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        class TargetPage(Base):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock dependencies
        mock_get_display_name = mocker.patch.object(
            TargetPage, "get_display_name", return_value="Target Page"
        )
        mock_layout = mocker.MagicMock()

        # Create page instance
        page = TestPage.__new__(TestPage)

        # Test add_to_page_button
        result = page.add_to_page_button(TargetPage, mock_layout)

        # Verify button creation and configuration
        mock_qpushbutton.assert_called_once_with("Target Page")
        mock_get_display_name.assert_called_once()
        mock_layout.addWidget.assert_called_once_with(mock_button_instance)
        mock_button_instance.clicked.connect.assert_called_once()

        # Verify return value
        assert_with_msg(result is mock_button_instance, "Should return button instance")
