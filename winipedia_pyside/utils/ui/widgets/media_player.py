"""Media player module.

This module contains the media player class.
"""

import time
from functools import partial
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from winipedia_pyside.utils.core.py_qiodevice import (
    EncryptedPyQFile,
    PyQFile,
    PyQIODevice,
)
from winipedia_pyside.utils.ui.base.base import Base as BaseUI
from winipedia_pyside.utils.ui.widgets.clickable_widget import ClickableVideoWidget


class MediaPlayer(QMediaPlayer):
    """Media player class."""

    def __init__(self, parent_layout: QLayout, *args: Any, **kwargs: Any) -> None:
        """Initialize the media player.

        Args:
            parent_layout: The parent layout to add the media player widget to.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.parent_layout = parent_layout
        self.io_device: PyQIODevice | None = None
        self.make_widget()

    def make_widget(self) -> None:
        """Make the widget.

        Creates the main media player widget with vertical layout, adds media controls
        above and below the video widget, and creates the video widget itself.
        """
        self.media_player_widget = QWidget()
        self.media_player_layout = QVBoxLayout(self.media_player_widget)
        self.parent_layout.addWidget(self.media_player_widget)
        self.add_media_controls_above()
        self.make_video_widget()
        self.add_media_controls_below()

    def make_video_widget(self) -> None:
        """Make the video widget.

        Creates a clickable video widget with expanding size policy, sets up
        audio output, and connects the click signal to toggle media controls.
        """
        self.video_widget = ClickableVideoWidget()
        self.video_widget.clicked.connect(self.on_video_clicked)
        self.video_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setVideoOutput(self.video_widget)

        self.audio_output = QAudioOutput()
        self.setAudioOutput(self.audio_output)

        self.media_player_layout.addWidget(self.video_widget)

    def on_video_clicked(self) -> None:
        """Handle video widget click.

        Toggles the visibility of media controls when the video widget is clicked.
        """
        if self.media_controls_widget_above.isVisible():
            self.hide_media_controls()
            return
        self.show_media_controls()

    def show_media_controls(self) -> None:
        """Show media controls.

        Makes both the above and below media control widgets visible.
        """
        self.media_controls_widget_above.show()
        self.media_controls_widget_below.show()

    def hide_media_controls(self) -> None:
        """Hide media controls.

        Hides both the above and below media control widgets.
        """
        self.media_controls_widget_above.hide()
        self.media_controls_widget_below.hide()

    def add_media_controls_above(self) -> None:
        """Add media controls above the video.

        Creates the top control bar with left, center, and right sections,
        then adds speed, volume, playback, and fullscreen controls.
        """
        # main above widget
        self.media_controls_widget_above = QWidget()
        self.media_controls_layout_above = QHBoxLayout(self.media_controls_widget_above)
        self.media_player_layout.addWidget(self.media_controls_widget_above)
        # left contorls
        self.left_controls_widget = QWidget()
        self.left_controls_layout = QHBoxLayout(self.left_controls_widget)
        self.media_controls_layout_above.addWidget(
            self.left_controls_widget, alignment=Qt.AlignmentFlag.AlignLeft
        )
        # center contorls
        self.center_controls_widget = QWidget()
        self.center_controls_layout = QHBoxLayout(self.center_controls_widget)
        self.media_controls_layout_above.addWidget(
            self.center_controls_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.right_controls_widget = QWidget()
        self.right_controls_layout = QHBoxLayout(self.right_controls_widget)
        self.media_controls_layout_above.addWidget(
            self.right_controls_widget, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.add_speed_control()
        self.add_volume_control()
        self.add_playback_control()
        self.add_fullscreen_control()

    def add_media_controls_below(self) -> None:
        """Add media controls below the video.

        Creates the bottom control bar and adds the progress control slider.
        """
        self.media_controls_widget_below = QWidget()
        self.media_controls_layout_below = QHBoxLayout(self.media_controls_widget_below)
        self.media_player_layout.addWidget(self.media_controls_widget_below)
        self.add_progress_control()

    def add_playback_control(self) -> None:
        """Add playback control.

        Creates a play/pause button with appropriate icons and connects it
        to the toggle_playback method. Adds the button to the center controls.
        """
        self.play_icon = BaseUI.get_svg_icon("play_icon")
        self.pause_icon = BaseUI.get_svg_icon("pause_icon")
        # Pause symbol: ⏸ (U+23F8)
        self.playback_button = QPushButton()
        self.playback_button.setIcon(self.pause_icon)
        self.playback_button.clicked.connect(self.toggle_playback)

        self.center_controls_layout.addWidget(self.playback_button)

    def toggle_playback(self) -> None:
        """Toggle playback.

        Switches between play and pause states, updating the button icon
        accordingly based on the current playback state.
        """
        if self.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
            self.playback_button.setIcon(self.play_icon)
        else:
            self.play()
            self.playback_button.setIcon(self.pause_icon)

    def add_speed_control(self) -> None:
        """Add speed control.

        Creates a button in the top left that shows a dropdown menu to select
        playback speed from predefined options (0.2x to 5x).
        """
        self.default_speed = 1
        self.speed_options = [0.2, 0.5, self.default_speed, 1.5, 2, 3, 4, 5]
        self.speed_button = QPushButton(f"{self.default_speed}x")
        self.speed_menu = QMenu(self.speed_button)
        for speed in self.speed_options:
            action = self.speed_menu.addAction(f"{speed}x")
            action.triggered.connect(partial(self.change_speed, speed))

        self.speed_button.setMenu(self.speed_menu)
        self.left_controls_layout.addWidget(self.speed_button)

    def change_speed(self, speed: float) -> None:
        """Change playback speed.

        Args:
            speed: The new playback speed multiplier.
        """
        self.setPlaybackRate(speed)
        self.speed_button.setText(f"{speed}x")

    def add_volume_control(self) -> None:
        """Add volume control.

        Creates a horizontal slider for volume control with range 0-100
        and connects it to the volume change handler.
        """
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.left_controls_layout.addWidget(self.volume_slider)

    def on_volume_changed(self, value: int) -> None:
        """Handle volume slider value change.

        Args:
            value: The new volume value from 0-100.
        """
        volume = value / 100.0  # Convert to 0.0-1.0 range
        self.audio_output.setVolume(volume)

    def add_fullscreen_control(self) -> None:
        """Add fullscreen control.

        Creates a fullscreen toggle button with appropriate icons and determines
        which widgets to hide/show when entering/exiting fullscreen mode.
        """
        self.fullscreen_icon = BaseUI.get_svg_icon("fullscreen_icon")
        self.exit_fullscreen_icon = BaseUI.get_svg_icon("exit_fullscreen_icon")
        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(self.fullscreen_icon)

        self.parent_widget = self.parent_layout.parentWidget()
        self.other_visible_widgets = [
            w
            for w in set(self.parent_widget.findChildren(QWidget))
            - {
                self.media_player_widget,
                *self.media_player_widget.findChildren(QWidget),
            }
            if w.isVisible() or not (w.isHidden() or w.isVisible())
        ]
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        self.right_controls_layout.addWidget(self.fullscreen_button)

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode.

        Switches between fullscreen and windowed mode, hiding/showing other
        widgets and updating the button icon accordingly.
        """
        # Get the main window
        main_window = self.media_player_widget.window()
        if main_window.isFullScreen():
            for widget in self.other_visible_widgets:
                widget.show()
            # show the window in the previous size
            main_window.showMaximized()
            self.fullscreen_button.setIcon(self.fullscreen_icon)
        else:
            for widget in self.other_visible_widgets:
                widget.hide()
            main_window.showFullScreen()
            self.fullscreen_button.setIcon(self.exit_fullscreen_icon)

    def add_progress_control(self) -> None:
        """Add progress control.

        Creates a horizontal progress slider and connects it to media player
        signals for position updates and user interaction handling.
        """
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.media_controls_layout_below.addWidget(self.progress_slider)

        # Connect media player signals to update the progress slider
        self.positionChanged.connect(self.update_slider_position)
        self.durationChanged.connect(self.set_slider_range)

        # Connect slider signals to update video position
        self.last_slider_moved_update = time.time()
        self.slider_moved_update_interval = 0.1
        self.progress_slider.sliderMoved.connect(self.on_slider_moved)
        self.progress_slider.sliderReleased.connect(self.on_slider_released)

    def update_slider_position(self, position: int) -> None:
        """Update the progress slider position.

        Args:
            position: The current media position in milliseconds.
        """
        # Only update if not being dragged to prevent jumps during manual sliding
        if not self.progress_slider.isSliderDown():
            self.progress_slider.setValue(position)

    def set_slider_range(self, duration: int) -> None:
        """Set the progress slider range based on media duration.

        Args:
            duration: The total media duration in milliseconds.
        """
        self.progress_slider.setRange(0, duration)

    def on_slider_moved(self, position: int) -> None:
        """Set the media position when slider is moved.

        Implements throttling to prevent excessive position updates during
        slider dragging for better performance.

        Args:
            position: The new position from the slider in milliseconds.
        """
        current_time = time.time()
        if (
            current_time - self.last_slider_moved_update
            > self.slider_moved_update_interval
        ):
            self.setPosition(position)
            self.last_slider_moved_update = current_time

    def on_slider_released(self) -> None:
        """Handle slider release event.

        Sets the final media position when the user releases the slider.
        """
        self.setPosition(self.progress_slider.value())

    def play_video(
        self,
        io_device: PyQIODevice,
        source_url: QUrl,
        position: int = 0,
    ) -> None:
        """Play the video.

        Stops current playback and starts a new video using the provided
        source function with a delay to prevent freezing.

        Args:
            io_device: The PyQIODevice to use as the media source.
            source_url: The QUrl representing the source location.
            position: The position to start playback from in milliseconds.
        """
        self.stop_and_close_io_device()

        self.resume_func = partial(self.resume_to_position, position=position)
        self.mediaStatusChanged.connect(self.resume_func)

        # SingleShot prevents freezing when starting new video while another is playing
        QTimer.singleShot(
            100,
            partial(
                self.set_source_and_play, io_device=io_device, source_url=source_url
            ),
        )

    def stop_and_close_io_device(self) -> None:
        """Stop playback and close the IO device."""
        self.stop()
        if self.io_device is not None:
            self.io_device.close()

    def resume_to_position(
        self, status: QMediaPlayer.MediaStatus, position: int
    ) -> None:
        """Resume playback to a position.

        Args:
            status: The current media status.
            position: The position to resume playback from in milliseconds.
        """
        if status == QMediaPlayer.MediaStatus.BufferedMedia:
            self.setPosition(position)
            self.mediaStatusChanged.disconnect(self.resume_func)

    def set_source_and_play(
        self,
        io_device: PyQIODevice,
        source_url: QUrl,
    ) -> None:
        """Set the source and play the video.

        Args:
            io_device: The PyQIODevice to use as the media source.
            source_url: The QUrl representing the source location.
        """
        self.set_source_device(io_device, source_url)
        self.play()

    def set_source_device(self, io_device: PyQIODevice, source_url: QUrl) -> None:
        """Set the source device for playback.

        Args:
            io_device: The PyQIODevice to use as the media source.
            source_url: The QUrl representing the source location.
        """
        self.source_url = source_url
        self.io_device = io_device
        self.setSourceDevice(self.io_device, self.source_url)

    def play_file(self, path: Path, position: int = 0) -> None:
        """Play a regular video file.

        Args:
            path: The file path to the video file to play.
            position: The position to start playback from in milliseconds.
        """
        self.play_video(
            position=position,
            io_device=PyQFile(path),
            source_url=QUrl.fromLocalFile(path),
        )

    def play_encrypted_file(
        self, path: Path, aes_gcm: AESGCM, position: int = 0
    ) -> None:
        """Play an encrypted video file.

        Args:
            path: The file path to the encrypted video file to play.
            aes_gcm: The AES-GCM cipher instance for decryption.
            position: The position to start playback from in milliseconds.
        """
        self.play_video(
            position=position,
            io_device=EncryptedPyQFile(path, aes_gcm),
            source_url=QUrl.fromLocalFile(path),
        )
