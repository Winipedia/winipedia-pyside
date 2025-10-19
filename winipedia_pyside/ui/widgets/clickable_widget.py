"""Clickable widget module.

This module contains clickable widget classes that emit signals when clicked.
Provides both regular QWidget and QVideoWidget variants with click functionality.
"""

from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget


class ClickableWidget(QWidget):
    """Widget that can be clicked.

    A QWidget subclass that emits a clicked signal when the left mouse
    button is pressed on the widget.
    """

    clicked = Signal()

    def mousePressEvent(self, event: Any) -> None:  # noqa: N802
        """Handle mouse press event.

        Emits the clicked signal when the left mouse button is pressed
        and passes the event to the parent class.

        Args:
            event: The mouse press event containing button and position information.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ClickableVideoWidget(QVideoWidget):
    """Video widget that can be clicked.

    A QVideoWidget subclass that emits a clicked signal when the left mouse
    button is pressed on the video widget.
    """

    clicked = Signal()

    def mousePressEvent(self, event: Any) -> None:  # noqa: N802
        """Handle mouse press event.

        Emits the clicked signal when the left mouse button is pressed
        and passes the event to the parent class.

        Args:
            event: The mouse press event containing button and position information.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
