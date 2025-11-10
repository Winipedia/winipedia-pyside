"""Tests for MediaPlayer widget."""

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QVBoxLayout
from pytest_mock import MockFixture
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg

from winipedia_pyside.utils.ui.widgets import media_player
from winipedia_pyside.utils.ui.widgets.media_player import MediaPlayer


class TestMediaPlayer:
    """Test class for MediaPlayer."""

    def test___init__(self, mocker: MockFixture) -> None:
        """Test method for __init__."""
        mock_make_widget = mocker.patch.object(MediaPlayer, "make_widget")
        parent_layout = QVBoxLayout()

        player = MediaPlayer(parent_layout)

        assert_with_msg(
            player.parent_layout is parent_layout, "Parent layout should be set"
        )
        mock_make_widget.assert_called_once()

    def test_make_widget(self, mocker: MockFixture) -> None:
        """Test method for make_widget."""
        # Mock the widget creation methods to avoid Qt widget issues
        mock_add_controls_above = mocker.patch.object(
            MediaPlayer, "add_media_controls_above"
        )
        mock_make_video_widget = mocker.patch.object(MediaPlayer, "make_video_widget")
        mock_add_controls_below = mocker.patch.object(
            MediaPlayer, "add_media_controls_below"
        )

        # Mock QWidget and QVBoxLayout to avoid Qt issues
        mock_qwidget = mocker.patch(make_obj_importpath(media_player) + ".QWidget")
        mock_qvboxlayout = mocker.patch(
            make_obj_importpath(media_player) + ".QVBoxLayout"
        )

        player = MediaPlayer.__new__(MediaPlayer)
        player.parent_layout = mocker.MagicMock()
        player.make_widget()

        mock_qwidget.assert_called_once()
        mock_qvboxlayout.assert_called_once()
        mock_add_controls_above.assert_called_once()
        mock_make_video_widget.assert_called_once()
        mock_add_controls_below.assert_called_once()

    def test_make_video_widget(self, mocker: MockFixture) -> None:
        """Test method for make_video_widget."""
        mock_clickable_widget = mocker.patch(
            make_obj_importpath(media_player) + ".ClickableVideoWidget"
        )
        mock_audio_output = mocker.patch(
            make_obj_importpath(media_player) + ".QAudioOutput"
        )

        player = MediaPlayer.__new__(MediaPlayer)
        player.media_player_layout = mocker.MagicMock()

        # Mock the Qt methods that require proper initialization
        mock_set_video_output = mocker.patch.object(player, "setVideoOutput")
        mock_set_audio_output = mocker.patch.object(player, "setAudioOutput")

        player.make_video_widget()

        assert_with_msg(hasattr(player, "video_widget"), "Should create video widget")
        assert_with_msg(hasattr(player, "audio_output"), "Should create audio output")
        mock_clickable_widget.assert_called_once()
        mock_audio_output.assert_called_once()
        mock_set_video_output.assert_called_once()
        mock_set_audio_output.assert_called_once()

    def test_on_video_clicked(self, mocker: MockFixture) -> None:
        """Test method for on_video_clicked."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_widget_above = mocker.MagicMock()
        player.media_controls_widget_above = mock_widget_above
        mock_hide = mocker.patch.object(player, "hide_media_controls")
        mock_show = mocker.patch.object(player, "show_media_controls")

        # Test when controls are visible - should hide
        mock_widget_above.isVisible.return_value = True
        player.on_video_clicked()
        mock_hide.assert_called_once()
        mock_show.assert_not_called()

        # Test when controls are hidden - should show
        mock_hide.reset_mock()
        mock_widget_above.isVisible.return_value = False
        player.on_video_clicked()
        mock_show.assert_called_once()

    def test_show_media_controls(self, mocker: MockFixture) -> None:
        """Test method for show_media_controls."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_widget_above = mocker.MagicMock()
        mock_widget_below = mocker.MagicMock()
        player.media_controls_widget_above = mock_widget_above
        player.media_controls_widget_below = mock_widget_below

        player.show_media_controls()

        mock_widget_above.show.assert_called_once()
        mock_widget_below.show.assert_called_once()

    def test_hide_media_controls(self, mocker: MockFixture) -> None:
        """Test method for hide_media_controls."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_widget_above = mocker.MagicMock()
        mock_widget_below = mocker.MagicMock()
        player.media_controls_widget_above = mock_widget_above
        player.media_controls_widget_below = mock_widget_below

        player.hide_media_controls()

        mock_widget_above.hide.assert_called_once()
        mock_widget_below.hide.assert_called_once()

    def test_add_media_controls_above(self, mocker: MockFixture) -> None:
        """Test method for add_media_controls_above."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.media_player_layout = mocker.MagicMock()

        # Mock Qt widget classes to avoid creating real widgets
        mock_qwidget = mocker.patch(make_obj_importpath(media_player) + ".QWidget")
        mock_qhboxlayout = mocker.patch(
            make_obj_importpath(media_player) + ".QHBoxLayout"
        )

        mock_add_speed = mocker.patch.object(player, "add_speed_control")
        mock_add_volume = mocker.patch.object(player, "add_volume_control")
        mock_add_playback = mocker.patch.object(player, "add_playback_control")
        mock_add_fullscreen = mocker.patch.object(player, "add_fullscreen_control")

        player.add_media_controls_above()

        # Verify Qt widgets were created
        expected_widget_count = 4
        assert_with_msg(
            mock_qwidget.call_count == expected_widget_count,
            f"Should create {expected_widget_count} QWidget instances",
        )
        assert_with_msg(
            mock_qhboxlayout.call_count == expected_widget_count,
            f"Should create {expected_widget_count} QHBoxLayout instances",
        )

        assert_with_msg(
            hasattr(player, "media_controls_widget_above"),
            "Should create above controls widget",
        )
        assert_with_msg(
            hasattr(player, "left_controls_widget"),
            "Should create left controls widget",
        )
        assert_with_msg(
            hasattr(player, "center_controls_widget"),
            "Should create center controls widget",
        )
        assert_with_msg(
            hasattr(player, "right_controls_widget"),
            "Should create right controls widget",
        )
        mock_add_speed.assert_called_once()
        mock_add_volume.assert_called_once()
        mock_add_playback.assert_called_once()
        mock_add_fullscreen.assert_called_once()

    def test_add_media_controls_below(self, mocker: MockFixture) -> None:
        """Test method for add_media_controls_below."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.media_player_layout = mocker.MagicMock()

        # Mock Qt widget classes to avoid creating real widgets
        mock_qwidget = mocker.patch(make_obj_importpath(media_player) + ".QWidget")
        mock_qhboxlayout = mocker.patch(
            make_obj_importpath(media_player) + ".QHBoxLayout"
        )

        mock_add_progress = mocker.patch.object(player, "add_progress_control")

        player.add_media_controls_below()

        # Verify Qt widgets were created
        mock_qwidget.assert_called_once()
        mock_qhboxlayout.assert_called_once()

        assert_with_msg(
            hasattr(player, "media_controls_widget_below"),
            "Should create below controls widget",
        )
        mock_add_progress.assert_called_once()

    def test_add_playback_control(self, mocker: MockFixture) -> None:
        """Test method for add_playback_control."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.center_controls_layout = mocker.MagicMock()
        mock_get_icon = mocker.patch(
            make_obj_importpath(media_player) + ".BaseUI.get_svg_icon"
        )
        mock_button = mocker.patch(make_obj_importpath(media_player) + ".QPushButton")

        player.add_playback_control()

        assert_with_msg(
            hasattr(player, "playback_button"), "Should create playback button"
        )
        mock_get_icon.assert_called()
        mock_button.assert_called_once()

    def test_toggle_playback(self, mocker: MockFixture) -> None:
        """Test method for toggle_playback."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_playback_button = mocker.MagicMock()
        mock_play_icon = mocker.MagicMock()
        mock_pause_icon = mocker.MagicMock()
        player.playback_button = mock_playback_button
        player.play_icon = mock_play_icon
        player.pause_icon = mock_pause_icon
        mock_pause = mocker.patch.object(player, "pause")
        mock_play = mocker.patch.object(player, "play")
        mock_playback_state = mocker.patch.object(player, "playbackState")

        # Test when playing - should pause
        mock_playback_state.return_value = QMediaPlayer.PlaybackState.PlayingState
        player.toggle_playback()
        mock_pause.assert_called_once()
        mock_playback_button.setIcon.assert_called_with(mock_play_icon)

        # Test when paused - should play
        mock_pause.reset_mock()
        mock_playback_button.setIcon.reset_mock()
        mock_playback_state.return_value = QMediaPlayer.PlaybackState.PausedState
        player.toggle_playback()
        mock_play.assert_called_once()
        mock_playback_button.setIcon.assert_called_with(mock_pause_icon)

    def test_add_speed_control(self, mocker: MockFixture) -> None:
        """Test method for add_speed_control."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.left_controls_layout = mocker.MagicMock()
        mock_button = mocker.patch(make_obj_importpath(media_player) + ".QPushButton")
        mock_menu = mocker.patch(make_obj_importpath(media_player) + ".QMenu")

        player.add_speed_control()

        assert_with_msg(hasattr(player, "speed_button"), "Should create speed button")
        assert_with_msg(hasattr(player, "speed_menu"), "Should create speed menu")
        assert_with_msg(hasattr(player, "speed_options"), "Should create speed options")
        mock_button.assert_called_once()
        mock_menu.assert_called_once()

    def test_change_speed(self, mocker: MockFixture) -> None:
        """Test method for change_speed."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_speed_button = mocker.MagicMock()
        player.speed_button = mock_speed_button
        mock_set_rate = mocker.patch.object(player, "setPlaybackRate")

        test_speed = 2.0
        player.change_speed(test_speed)

        mock_set_rate.assert_called_once_with(test_speed)
        mock_speed_button.setText.assert_called_once_with(f"{test_speed}x")

    def test_add_volume_control(self, mocker: MockFixture) -> None:
        """Test method for add_volume_control."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.left_controls_layout = mocker.MagicMock()
        mock_slider = mocker.patch(make_obj_importpath(media_player) + ".QSlider")

        player.add_volume_control()

        assert_with_msg(hasattr(player, "volume_slider"), "Should create volume slider")
        mock_slider.assert_called_once()

    def test_on_volume_changed(self, mocker: MockFixture) -> None:
        """Test method for on_volume_changed."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_audio_output = mocker.MagicMock()
        player.audio_output = mock_audio_output

        test_volume = 75
        player.on_volume_changed(test_volume)

        mock_audio_output.setVolume.assert_called_once_with(test_volume / 100)

    def test_add_fullscreen_control(self, mocker: MockFixture) -> None:
        """Test method for add_fullscreen_control."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.right_controls_layout = mocker.MagicMock()
        player.parent_layout = mocker.MagicMock()
        player.media_player_widget = mocker.MagicMock()
        mock_get_icon = mocker.patch(
            make_obj_importpath(media_player) + ".BaseUI.get_svg_icon"
        )
        mock_button = mocker.patch(make_obj_importpath(media_player) + ".QPushButton")

        player.add_fullscreen_control()

        assert_with_msg(
            hasattr(player, "fullscreen_button"), "Should create fullscreen button"
        )
        mock_get_icon.assert_called()
        mock_button.assert_called_once()

    def test_toggle_fullscreen(self, mocker: MockFixture) -> None:
        """Test method for toggle_fullscreen."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_fullscreen_button = mocker.MagicMock()
        mock_fullscreen_icon = mocker.MagicMock()
        mock_exit_fullscreen_icon = mocker.MagicMock()
        mock_media_player_widget = mocker.MagicMock()
        player.fullscreen_button = mock_fullscreen_button
        player.fullscreen_icon = mock_fullscreen_icon
        player.exit_fullscreen_icon = mock_exit_fullscreen_icon
        player.media_player_widget = mock_media_player_widget
        player.other_visible_widgets = []

        # Mock the main window
        main_window = mocker.MagicMock()
        mock_media_player_widget.window.return_value = main_window

        # Test entering fullscreen (main window is not fullscreen)
        main_window.isFullScreen.return_value = False
        player.toggle_fullscreen()
        main_window.showFullScreen.assert_called_once()
        mock_fullscreen_button.setIcon.assert_called_with(mock_exit_fullscreen_icon)

        # Test exiting fullscreen (main window is fullscreen)
        main_window.isFullScreen.return_value = True
        main_window.showFullScreen.reset_mock()
        mock_fullscreen_button.setIcon.reset_mock()
        player.toggle_fullscreen()
        main_window.showMaximized.assert_called_once()
        mock_fullscreen_button.setIcon.assert_called_with(mock_fullscreen_icon)

    def test_add_progress_control(self, mocker: MockFixture) -> None:
        """Test method for add_progress_control."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.media_controls_layout_below = mocker.MagicMock()
        mock_slider = mocker.patch(make_obj_importpath(media_player) + ".QSlider")
        mock_position_changed = mocker.patch.object(player, "positionChanged")
        mock_duration_changed = mocker.patch.object(player, "durationChanged")

        player.add_progress_control()

        assert_with_msg(
            hasattr(player, "progress_slider"), "Should create progress slider"
        )
        mock_slider.assert_called_once()
        mock_position_changed.connect.assert_called_once()
        mock_duration_changed.connect.assert_called_once()

    def test_update_slider_position(self, mocker: MockFixture) -> None:
        """Test method for update_slider_position."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_progress_slider = mocker.MagicMock()
        player.progress_slider = mock_progress_slider

        # Mock slider not being dragged
        mock_progress_slider.isSliderDown.return_value = False

        test_position = 5000
        player.update_slider_position(test_position)

        mock_progress_slider.setValue.assert_called_once_with(test_position)

        # Test when slider is being dragged - should not update
        mock_progress_slider.isSliderDown.return_value = True
        mock_progress_slider.setValue.reset_mock()
        player.update_slider_position(test_position)
        mock_progress_slider.setValue.assert_not_called()

    def test_set_slider_range(self, mocker: MockFixture) -> None:
        """Test method for set_slider_range."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_progress_slider = mocker.MagicMock()
        player.progress_slider = mock_progress_slider

        test_duration = 10000
        player.set_slider_range(test_duration)

        mock_progress_slider.setRange.assert_called_once_with(0, test_duration)

    def test_on_slider_moved(self, mocker: MockFixture) -> None:
        """Test method for on_slider_moved."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.last_slider_moved_update = 0
        player.slider_moved_update_interval = 0.1
        mock_time = mocker.patch(make_obj_importpath(media_player) + ".time")
        mock_set_position = mocker.patch.object(player, "setPosition")

        # Test when enough time has passed
        mock_time.time.return_value = 1.0
        test_position = 3000
        player.on_slider_moved(test_position)

        mock_set_position.assert_called_once_with(test_position)
        assert_with_msg(
            player.last_slider_moved_update == 1.0,
            "Should update last slider moved time",
        )

    def test_on_slider_released(self, mocker: MockFixture) -> None:
        """Test method for on_slider_released."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_progress_slider = mocker.MagicMock()
        player.progress_slider = mock_progress_slider
        mock_set_position = mocker.patch.object(player, "setPosition")

        test_position = 4000
        mock_progress_slider.value.return_value = test_position
        player.on_slider_released()

        mock_set_position.assert_called_once_with(test_position)

    def test_play_video(self, mocker: MockFixture) -> None:
        """Test method for play_video."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.io_device = None  # Initialize the attribute that __init__ would set
        mock_stop_and_close = mocker.patch.object(player, "stop_and_close_io_device")
        mock_media_status_changed = mocker.patch.object(player, "mediaStatusChanged")
        mock_timer = mocker.patch(make_obj_importpath(media_player) + ".QTimer")
        mock_partial = mocker.patch(make_obj_importpath(media_player) + ".partial")

        io_device = mocker.MagicMock()
        source_url = QUrl("file:///test.mp4")
        position = 1000

        player.play_video(io_device, source_url, position)

        mock_stop_and_close.assert_called_once()
        mock_media_status_changed.connect.assert_called_once()
        mock_timer.singleShot.assert_called_once()
        mock_partial.assert_called()

    def test_stop_and_close_io_device(self, mocker: MockFixture) -> None:
        """Test method for stop_and_close_io_device."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_stop = mocker.patch.object(player, "stop")
        mock_io_device = mocker.MagicMock()
        player.io_device = mock_io_device

        player.stop_and_close_io_device()

        mock_stop.assert_called_once()
        mock_io_device.close.assert_called_once()

        # Test with None io_device
        player.io_device = None
        player.stop_and_close_io_device()  # Should not raise an error

    def test_resume_to_position(self, mocker: MockFixture) -> None:
        """Test method for resume_to_position."""
        player = MediaPlayer.__new__(MediaPlayer)
        player.resume_func = mocker.MagicMock()
        mock_set_position = mocker.patch.object(player, "setPosition")
        mock_media_status_changed = mocker.patch.object(player, "mediaStatusChanged")

        position = 2000
        status = QMediaPlayer.MediaStatus.BufferedMedia

        player.resume_to_position(status, position)

        mock_set_position.assert_called_once_with(position)
        mock_media_status_changed.disconnect.assert_called_once_with(player.resume_func)

    def test_set_source_and_play(self, mocker: MockFixture) -> None:
        """Test method for set_source_and_play."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_set_source = mocker.patch.object(player, "set_source_device")
        mock_play = mocker.patch.object(player, "play")

        io_device = mocker.MagicMock()
        source_url = QUrl("file:///test.mp4")

        player.set_source_and_play(io_device, source_url)

        mock_set_source.assert_called_once_with(io_device, source_url)
        mock_play.assert_called_once()

    def test_set_source_device(self, mocker: MockFixture) -> None:
        """Test method for set_source_device."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_set_source_device = mocker.patch.object(player, "setSourceDevice")

        io_device = mocker.MagicMock()
        source_url = QUrl("file:///test.mp4")

        player.set_source_device(io_device, source_url)

        assert_with_msg(player.source_url == source_url, "Should set source URL")
        assert_with_msg(player.io_device == io_device, "Should set IO device")
        mock_set_source_device.assert_called_once_with(io_device, source_url)

    def test_play_file(self, mocker: MockFixture) -> None:
        """Test method for play_file."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_play_video = mocker.patch.object(player, "play_video")
        mock_pyq_file = mocker.patch(make_obj_importpath(media_player) + ".PyQFile")
        mock_qurl = mocker.patch(make_obj_importpath(media_player) + ".QUrl")

        test_path = Path("/test/video.mp4")
        position = 500

        player.play_file(test_path, position)

        mock_pyq_file.assert_called_once_with(test_path)
        mock_qurl.fromLocalFile.assert_called_once_with(test_path)
        mock_play_video.assert_called_once()

    def test_play_encrypted_file(self, mocker: MockFixture) -> None:
        """Test method for play_encrypted_file."""
        player = MediaPlayer.__new__(MediaPlayer)
        mock_play_video = mocker.patch.object(player, "play_video")
        mock_encrypted_file = mocker.patch(
            make_obj_importpath(media_player) + ".EncryptedPyQFile"
        )
        mock_qurl = mocker.patch(make_obj_importpath(media_player) + ".QUrl")

        test_path = Path("/test/encrypted.mp4")
        aes_gcm = mocker.MagicMock()
        position = 750

        player.play_encrypted_file(test_path, aes_gcm, position)

        mock_encrypted_file.assert_called_once_with(test_path, aes_gcm)
        mock_qurl.fromLocalFile.assert_called_once_with(test_path)
        mock_play_video.assert_called_once()
