"""Tests for Base window class."""

from typing import final

from pytest_mock import MockFixture
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg

from winipedia_pyside.utils.ui.pages.base.base import Base as BasePage
from winipedia_pyside.utils.ui.windows.base import base as windows_base
from winipedia_pyside.utils.ui.windows.base.base import Base


class TestBase:
    """Test class for Base."""

    def test_get_start_page_cls(self) -> None:
        """Test method for get_start_page_cls."""

        # Create a mock page class
        class MockPage(BasePage):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Create a concrete test class that implements the abstract methods
        class TestWindow(Base):
            @classmethod
            @final
            def get_all_page_classes(cls) -> list[type[BasePage]]:
                return [MockPage]

            @classmethod
            @final
            def get_start_page_cls(cls) -> type[BasePage]:
                return MockPage

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Test that the method returns the expected page class
        assert_with_msg(
            TestWindow.get_start_page_cls() is MockPage,
            "get_start_page_cls should return the expected page class",
        )

    def test_base_setup(self, mocker: MockFixture) -> None:
        """Test method for base_setup."""

        # Create a mock page class
        class MockPage(BasePage):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Create a concrete test class
        class TestWindow(Base):
            @classmethod
            @final
            def get_all_page_classes(cls) -> list[type[BasePage]]:
                return [MockPage]

            @classmethod
            @final
            def get_start_page_cls(cls) -> type[BasePage]:
                return MockPage

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock all Qt components to avoid creating real widgets
        mocker.patch("PySide6.QtWidgets.QMainWindow.__init__")
        mock_set_window_title = mocker.patch.object(TestWindow, "setWindowTitle")
        mock_set_central_widget = mocker.patch.object(TestWindow, "setCentralWidget")
        mock_qstacked_widget = mocker.patch(
            make_obj_importpath(windows_base) + ".QStackedWidget"
        )
        mock_make_pages = mocker.patch.object(TestWindow, "make_pages")
        mock_set_start_page = mocker.patch.object(TestWindow, "set_start_page")
        mock_get_display_name = mocker.patch.object(
            TestWindow, "get_display_name", return_value="Test Window"
        )

        # Create window instance without calling __init__
        window = TestWindow.__new__(TestWindow)

        # Call base_setup directly to test its functionality
        window.base_setup()

        # Verify all expected calls were made
        mock_get_display_name.assert_called_once()
        mock_set_window_title.assert_called_once_with("Test Window")
        mock_qstacked_widget.assert_called_once()
        mock_set_central_widget.assert_called_once()
        mock_make_pages.assert_called_once()
        mock_set_start_page.assert_called_once()

        # Verify stack attribute is created
        assert_with_msg(
            hasattr(window, "stack"), "base_setup should create stack attribute"
        )

    def test_add_page(self, mocker: MockFixture) -> None:
        """Test method for add_page."""

        # Create a mock page class
        class MockPage(BasePage):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Create a concrete test class
        class TestWindow(Base):
            @classmethod
            @final
            def get_all_page_classes(cls) -> list[type[BasePage]]:
                return [MockPage]

            @classmethod
            @final
            def get_start_page_cls(cls) -> type[BasePage]:
                return MockPage

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock Qt components
        mocker.patch("PySide6.QtWidgets.QMainWindow.__init__")
        mock_stack = mocker.MagicMock()
        mock_page = mocker.MagicMock()

        # Create window instance
        window = TestWindow.__new__(TestWindow)
        window.stack = mock_stack

        # Test add_page functionality
        window.add_page(mock_page)

        # Verify page was added to stack
        mock_stack.addWidget.assert_called_once_with(mock_page)

    def test_get_all_page_classes(self) -> None:
        """Test method for get_all_page_classes."""

        # Create a mock page class
        class MockPage(BasePage):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Create a concrete test class that implements the abstract method
        class TestWindow(Base):
            @classmethod
            @final
            def get_all_page_classes(cls) -> list[type[BasePage]]:
                return [MockPage]

            @classmethod
            @final
            def get_start_page_cls(cls) -> type[BasePage]:
                return MockPage

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Test that the method returns the expected page classes
        page_classes = TestWindow.get_all_page_classes()
        assert_with_msg(
            len(page_classes) == 1,
            "get_all_page_classes should return one page class",
        )
        assert_with_msg(
            page_classes[0] is MockPage,
            "get_all_page_classes should return the expected page class",
        )

    def test_make_pages(self, mocker: MockFixture) -> None:
        """Test method for make_pages."""

        # Create a simple mock page class
        class MockPage(BasePage):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Create a concrete test class
        class TestWindow(Base):
            @classmethod
            @final
            def get_all_page_classes(cls) -> list[type[BasePage]]:
                return [MockPage]

            @classmethod
            @final
            def get_start_page_cls(cls) -> type[BasePage]:
                return MockPage

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock Qt components and page instantiation
        mocker.patch("PySide6.QtWidgets.QMainWindow.__init__")

        # Mock the MockPage constructor to avoid actual page creation
        mocker.patch.object(MockPage, "__init__", return_value=None)

        # Create window instance
        window = TestWindow.__new__(TestWindow)

        # Test make_pages functionality
        window.make_pages()

    def test_set_start_page(self, mocker: MockFixture) -> None:
        """Test method for set_start_page."""

        # Create a mock page class
        class MockPage(BasePage):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Create a concrete test class
        class TestWindow(Base):
            @classmethod
            @final
            def get_all_page_classes(cls) -> list[type[BasePage]]:
                return [MockPage]

            @classmethod
            @final
            def get_start_page_cls(cls) -> type[BasePage]:
                return MockPage

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock Qt components
        mocker.patch("PySide6.QtWidgets.QMainWindow.__init__")

        # Mock set_current_page method
        mock_set_current_page = mocker.patch.object(TestWindow, "set_current_page")

        # Create window instance
        window = TestWindow.__new__(TestWindow)

        # Test set_start_page functionality
        window.set_start_page()

        # Verify set_current_page was called with the start page class
        mock_set_current_page.assert_called_once_with(MockPage)
