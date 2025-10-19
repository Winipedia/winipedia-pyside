"""Tests for winipedia_pyside.ui.pages.player module."""

from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtWidgets import QVBoxLayout
from pytest_mock import MockerFixture
from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.ui.pages.player import Player


class TestPlayer:
    """Test class for Player."""

    def test_start_playback(self) -> None:
        """Test method for start_playback."""
        # Test that the method exists in the class
        assert_with_msg(
            hasattr(Player, "start_playback"),
            "Player should have start_playback method",
        )
        assert_with_msg(
            callable(Player.start_playback), "start_playback should be callable"
        )

        # Test that start_playback is abstract by checking the method
        assert_with_msg(
            getattr(Player.start_playback, "__isabstractmethod__", False),
            "start_playback should be marked as abstract method",
        )

    def test_setup(self, mocker: MockerFixture) -> None:
        """Test method for setup."""
        # Mock the MediaPlayer class
        mock_media_player_class = mocker.patch(
            "winipedia_pyside.ui.pages.player.MediaPlayer"
        )
        mock_media_player_instance = mocker.MagicMock()
        mock_media_player_class.return_value = mock_media_player_instance

        # Create a mock player instance with v_layout
        mock_player = mocker.MagicMock(spec=Player)
        mock_layout = mocker.MagicMock(spec=QVBoxLayout)
        mock_player.v_layout = mock_layout

        # Call setup method directly on the class
        Player.setup(mock_player)

        # Verify MediaPlayer was instantiated with correct layout
        mock_media_player_class.assert_called_once_with(mock_layout)

        # Verify the media player was assigned to the media_player attribute
        assert_with_msg(
            mock_player.media_player is mock_media_player_instance,
            "setup should assign MediaPlayer instance to media_player attribute",
        )

        # Test that setup method exists and is final
        assert_with_msg(hasattr(Player, "setup"), "Player should have setup method")
        assert_with_msg(callable(Player.setup), "setup should be callable")

    def test_play_file_from_func(self, mocker: MockerFixture) -> None:
        """Test method for play_file_from_func."""
        # Create a mock player instance
        mock_player = mocker.MagicMock(spec=Player)

        # Mock the set_current_page method
        mock_set_current_page = mocker.patch.object(mock_player, "set_current_page")

        # Create a mock play function
        mock_play_func = mocker.MagicMock()

        # Test data
        test_path = Path("test_video.mp4")
        test_position = 1000
        test_kwargs = {"extra_arg": "test_value"}

        # Call play_file_from_func method directly on the class
        Player.play_file_from_func(
            mock_player,
            play_func=mock_play_func,
            path=test_path,
            position=test_position,
            **test_kwargs,
        )

        # Verify set_current_page was called with the Player class
        # When calling Player.play_file_from_func(), self.__class__ refers to Player
        mock_set_current_page.assert_called_once_with(Player)

        # Verify the play function was called with correct arguments
        mock_play_func.assert_called_once_with(
            path=test_path, position=test_position, extra_arg="test_value"
        )

        # Test that the method exists and is final
        assert_with_msg(
            hasattr(Player, "play_file_from_func"),
            "Player should have play_file_from_func method",
        )
        assert_with_msg(
            callable(Player.play_file_from_func),
            "play_file_from_func should be callable",
        )

    def test_play_file(self, mocker: MockerFixture) -> None:
        """Test method for play_file."""
        # Create a mock player instance with media_player
        mock_player = mocker.MagicMock(spec=Player)
        mock_media_player = mocker.MagicMock()
        mock_player.media_player = mock_media_player

        # Mock the play_file_from_func method
        mock_play_file_from_func = mocker.patch.object(
            mock_player, "play_file_from_func"
        )

        # Test data
        test_path = Path("test_video.mp4")
        test_position = 2000

        # Call play_file method directly on the class
        Player.play_file(mock_player, path=test_path, position=test_position)

        # Verify play_file_from_func was called with media_player.play_file
        mock_play_file_from_func.assert_called_once_with(
            mock_media_player.play_file, path=test_path, position=test_position
        )

        # Test that the method exists and is final
        assert_with_msg(
            hasattr(Player, "play_file"),
            "Player should have play_file method",
        )
        assert_with_msg(
            callable(Player.play_file),
            "play_file should be callable",
        )

    def test_play_encrypted_file(self, mocker: MockerFixture) -> None:
        """Test method for play_encrypted_file."""
        # Create a mock player instance with media_player
        mock_player = mocker.MagicMock(spec=Player)
        mock_media_player = mocker.MagicMock()
        mock_player.media_player = mock_media_player

        # Mock the play_file_from_func method
        mock_play_file_from_func = mocker.patch.object(
            mock_player, "play_file_from_func"
        )

        # Test data
        test_path = Path("encrypted_video.mp4")
        test_position = 3000
        test_aes_gcm = mocker.MagicMock(spec=AESGCM)

        # Call play_encrypted_file method directly on the class
        Player.play_encrypted_file(
            mock_player, path=test_path, aes_gcm=test_aes_gcm, position=test_position
        )

        # Verify play_file_from_func was called with media_player.play_encrypted_file
        mock_play_file_from_func.assert_called_once_with(
            mock_media_player.play_encrypted_file,
            path=test_path,
            position=test_position,
            aes_gcm=test_aes_gcm,
        )

        # Test that the method exists and is final
        assert_with_msg(
            hasattr(Player, "play_encrypted_file"),
            "Player should have play_encrypted_file method",
        )
        assert_with_msg(
            callable(Player.play_encrypted_file),
            "play_encrypted_file should be callable",
        )
