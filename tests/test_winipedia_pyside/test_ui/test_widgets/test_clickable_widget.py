"""Tests for ClickableWidget and ClickableVideoWidget."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget
from pytest_mock import MockFixture
from pytestqt.qtbot import QtBot
from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.ui.widgets.clickable_widget import (
    ClickableVideoWidget,
    ClickableWidget,
)


class TestClickableWidget:
    """Test class for ClickableWidget."""

    @pytest.mark.skip
    def test_mousePressEvent(self, qtbot: QtBot, mocker: MockFixture) -> None:  # noqa: N802
        """Test method for mousePressEvent."""
        # Create widget and add to qtbot
        widget = ClickableWidget()
        qtbot.addWidget(widget)

        # Use qtbot's signal spy to track signal emissions
        signal_spy = qtbot.waitSignal(widget.clicked, timeout=1000, raising=False)

        # Mock the parent mousePressEvent
        mock_super = mocker.patch.object(QWidget, "mousePressEvent")

        # Create a left mouse button press event
        left_click_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            widget.rect().center(),
            widget.rect().center(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        # Call mousePressEvent
        widget.mousePressEvent(left_click_event)

        # Verify clicked signal was emitted
        assert_with_msg(
            signal_spy.signal_triggered,
            "Clicked signal should be emitted for left click",
        )

        # Verify parent mousePressEvent was called
        mock_super.assert_called_once_with(left_click_event)

        # Test with right mouse button (should not emit clicked signal)
        mock_super.reset_mock()

        # Create a new signal spy for the right click test
        signal_spy_right = qtbot.waitSignal(widget.clicked, timeout=100, raising=False)

        right_click_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            widget.rect().center(),
            widget.rect().center(),
            Qt.MouseButton.RightButton,
            Qt.MouseButton.RightButton,
            Qt.KeyboardModifier.NoModifier,
        )

        widget.mousePressEvent(right_click_event)

        # Verify clicked signal was NOT emitted for right click
        assert_with_msg(
            not signal_spy_right.signal_triggered,
            "Clicked signal should NOT be emitted for right click",
        )

        # Verify parent mousePressEvent was still called
        mock_super.assert_called_once_with(right_click_event)

    @pytest.mark.skip
    def test_clicked_signal_exists(self, qtbot: QtBot) -> None:
        """Test that clicked signal exists and is properly defined."""
        widget = ClickableWidget()
        qtbot.addWidget(widget)

        assert_with_msg(
            hasattr(widget, "clicked"), "ClickableWidget should have clicked signal"
        )
        assert_with_msg(
            widget.clicked.__class__.__name__ == "SignalInstance",
            "clicked should be a Qt signal",
        )


class TestClickableVideoWidget:
    """Test class for ClickableVideoWidget."""

    @pytest.mark.skip
    def test_mousePressEvent(self, qtbot: QtBot, mocker: MockFixture) -> None:  # noqa: N802
        """Test method for mousePressEvent."""
        # Create video widget and add to qtbot
        widget = ClickableVideoWidget()
        qtbot.addWidget(widget)

        # Use qtbot's signal spy to track signal emissions
        signal_spy = qtbot.waitSignal(widget.clicked, timeout=1000, raising=False)

        # Mock the parent mousePressEvent (QVideoWidget's mousePressEvent)
        mock_super = mocker.patch.object(
            ClickableVideoWidget.__bases__[0], "mousePressEvent"
        )

        # Create a left mouse button press event
        left_click_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            widget.rect().center(),
            widget.rect().center(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        # Call mousePressEvent
        widget.mousePressEvent(left_click_event)

        # Verify clicked signal was emitted
        assert_with_msg(
            signal_spy.signal_triggered,
            "Clicked signal should be emitted for left click",
        )

        # Verify parent mousePressEvent was called
        mock_super.assert_called_once_with(left_click_event)

        # Test with right mouse button (should not emit clicked signal)
        mock_super.reset_mock()

        # Create a new signal spy for the right click test
        signal_spy_right = qtbot.waitSignal(widget.clicked, timeout=100, raising=False)

        right_click_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            widget.rect().center(),
            widget.rect().center(),
            Qt.MouseButton.RightButton,
            Qt.MouseButton.RightButton,
            Qt.KeyboardModifier.NoModifier,
        )

        widget.mousePressEvent(right_click_event)

        # Verify clicked signal was NOT emitted for right click
        assert_with_msg(
            not signal_spy_right.signal_triggered,
            "Clicked signal should NOT be emitted for right click",
        )

        # Verify parent mousePressEvent was still called
        mock_super.assert_called_once_with(right_click_event)

    @pytest.mark.skip
    def test_clicked_signal_exists(self, qtbot: QtBot) -> None:
        """Test that clicked signal exists and is properly defined."""
        widget = ClickableVideoWidget()
        qtbot.addWidget(widget)

        assert_with_msg(
            hasattr(widget, "clicked"),
            "ClickableVideoWidget should have clicked signal",
        )
        assert_with_msg(
            widget.clicked.__class__.__name__ == "SignalInstance",
            "clicked should be a Qt signal",
        )
