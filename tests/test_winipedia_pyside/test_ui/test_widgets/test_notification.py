"""Tests for Notification widget."""

from pyqttoast import ToastIcon  # type: ignore[import-untyped]
from pytest_mock import MockFixture
from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.ui.widgets.notification import Notification


class TestNotification:
    """Test class for Notification."""

    def test___init__(self, mocker: MockFixture) -> None:
        """Test method for __init__."""
        # Mock the Toast parent class and its methods
        mock_toast_init = mocker.patch("pyqttoast.Toast.__init__")
        mock_active_window = mocker.patch(
            "winipedia_pyside.ui.widgets.notification.QApplication.activeWindow"
        )
        mock_window = mocker.MagicMock()
        mock_active_window.return_value = mock_window

        # Mock the notification methods to avoid actual Qt operations
        mock_set_duration = mocker.patch.object(Notification, "setDuration")
        mock_set_icon = mocker.patch.object(Notification, "setIcon")
        mock_set_title = mocker.patch.object(Notification, "set_title")
        mock_set_text = mocker.patch.object(Notification, "set_text")

        # Test with default parameters
        title = "Test Title"
        text = "Test notification text"
        Notification(title, text)

        # Verify parent initialization
        mock_toast_init.assert_called_once_with(mock_window)

        # Verify default settings
        mock_set_duration.assert_called_once_with(10000)  # Default duration
        mock_set_icon.assert_called_once_with(ToastIcon.INFORMATION)  # Default icon
        mock_set_title.assert_called_once_with(title)
        mock_set_text.assert_called_once_with(text)

        # Test with custom parameters
        mock_toast_init.reset_mock()
        mock_set_duration.reset_mock()
        mock_set_icon.reset_mock()
        mock_set_title.reset_mock()
        mock_set_text.reset_mock()

        custom_title = "Custom Title"
        custom_text = "Custom text"
        custom_icon = ToastIcon.WARNING
        custom_duration = 5000

        Notification(custom_title, custom_text, custom_icon, custom_duration)

        mock_toast_init.assert_called_once_with(mock_window)
        mock_set_duration.assert_called_once_with(custom_duration)
        mock_set_icon.assert_called_once_with(custom_icon)
        mock_set_title.assert_called_once_with(custom_title)
        mock_set_text.assert_called_once_with(custom_text)

    def test_set_title(self, mocker: MockFixture) -> None:
        """Test method for set_title."""
        # Mock all dependencies first
        mocker.patch("pyqttoast.Toast.__init__")
        mocker.patch(
            "winipedia_pyside.ui.widgets.notification.QApplication.activeWindow"
        )
        mocker.patch.object(Notification, "setDuration")
        mocker.patch.object(Notification, "setIcon")

        # Mock the methods we want to test
        mock_str_to_half_window_width = mocker.patch.object(
            Notification, "str_to_half_window_width"
        )
        mock_set_title_qt = mocker.patch.object(Notification, "setTitle")

        # Create notification instance
        notification = Notification.__new__(Notification)

        # Test set_title functionality
        test_title = "Test Title"
        truncated_title = "Test Ti..."
        mock_str_to_half_window_width.return_value = truncated_title

        notification.set_title(test_title)

        mock_str_to_half_window_width.assert_called_once_with(test_title)
        mock_set_title_qt.assert_called_once_with(truncated_title)

    def test_set_text(self, mocker: MockFixture) -> None:
        """Test method for set_text."""
        # Mock all dependencies first
        mocker.patch("pyqttoast.Toast.__init__")
        mocker.patch(
            "winipedia_pyside.ui.widgets.notification.QApplication.activeWindow"
        )
        mocker.patch.object(Notification, "setDuration")
        mocker.patch.object(Notification, "setIcon")

        # Mock the methods we want to test
        mock_str_to_half_window_width = mocker.patch.object(
            Notification, "str_to_half_window_width"
        )
        mock_set_text_qt = mocker.patch.object(Notification, "setText")

        # Create notification instance
        notification = Notification.__new__(Notification)

        # Test set_text functionality
        test_text = "This is a long notification text that might need truncation"
        truncated_text = "This is a long notification text..."
        mock_str_to_half_window_width.return_value = truncated_text

        notification.set_text(test_text)

        mock_str_to_half_window_width.assert_called_once_with(test_text)
        mock_set_text_qt.assert_called_once_with(truncated_text)

    def test_str_to_half_window_width(self, mocker: MockFixture) -> None:
        """Test method for str_to_half_window_width."""
        # Create notification instance with mocked parent
        mocker.patch("pyqttoast.Toast.__init__")
        mocker.patch.object(Notification, "setDuration")
        mocker.patch.object(Notification, "setIcon")
        mocker.patch.object(Notification, "set_title")
        mocker.patch.object(Notification, "set_text")

        # Mock QApplication.activeWindow and value_to_truncated_string
        mock_active_window = mocker.patch(
            "winipedia_pyside.ui.widgets.notification.QApplication.activeWindow"
        )
        mock_truncate = mocker.patch(
            "winipedia_pyside.ui.widgets.notification.value_to_truncated_string"
        )

        notification = Notification("title", "text")

        # Test with active window
        mock_window = mocker.MagicMock()
        mock_window.width.return_value = 1000
        mock_active_window.return_value = mock_window
        mock_truncate.return_value = "truncated text"

        test_string = "This is a test string"
        result = notification.str_to_half_window_width(test_string)

        expected_width = 500  # 1000 / 2
        mock_truncate.assert_called_once_with(test_string, expected_width)
        assert_with_msg(result == "truncated text", "Should return truncated text")

        # Test with no active window (fallback to 500)
        mock_active_window.return_value = None
        mock_truncate.reset_mock()
        mock_truncate.return_value = "fallback truncated"

        result2 = notification.str_to_half_window_width(test_string)

        mock_truncate.assert_called_once_with(test_string, 500)  # Fallback width
        assert_with_msg(result2 == "fallback truncated", "Should use fallback width")
