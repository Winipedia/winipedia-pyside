"""Notification module.

This module contains functions to show notifications.
"""

from pyqttoast import Toast, ToastIcon, ToastPosition  # type: ignore[import-untyped]
from PySide6.QtWidgets import QApplication
from winipedia_utils.utils.data.structures.text.string import value_to_truncated_string

Toast.setPosition(ToastPosition.TOP_MIDDLE)


class Notification(Toast):  # type: ignore[misc]
    """Notification class."""

    def __init__(
        self,
        title: str,
        text: str,
        icon: ToastIcon = ToastIcon.INFORMATION,
        duration: int = 10000,
    ) -> None:
        """Initialize the notification.

        The notification is shown in the top middle of the screen.

        Args:
            title: The title of the notification.
            text: The text of the notification.
            icon: The icon of the notification. Defaults to INFORMATION.
            duration: The duration of the notification in milliseconds.
                        Defaults to 10000.
        """
        super().__init__(QApplication.activeWindow())
        self.setDuration(duration)
        self.setIcon(icon)
        self.set_title(title)
        self.set_text(text)

    def set_title(self, title: str) -> None:
        """Set the title of the notification.

        Truncates the title to fit within half the window width before setting it.

        Args:
            title: The title text to set.
        """
        title = self.str_to_half_window_width(title)
        self.setTitle(title)

    def set_text(self, text: str) -> None:
        """Set the text of the notification.

        Truncates the text to fit within half the window width before setting it.

        Args:
            text: The notification text to set.
        """
        text = self.str_to_half_window_width(text)
        self.setText(text)

    def str_to_half_window_width(self, string: str) -> str:
        """Truncate the string to the width of the active window.

        Calculates half the width of the active window and truncates the string
        to fit within that width. Falls back to 500 pixels if no active window.

        Args:
            string: The string to truncate.

        Returns:
            The truncated string that fits within half the window width.
        """
        main_window = QApplication.activeWindow()
        width = main_window.width() / 2 if main_window is not None else 500
        width = int(width)
        return value_to_truncated_string(string, width)
