"""Player page module.

This module contains the player page class for the VideoVault application.
"""

from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from winipedia_pyside.utils.ui.pages.base.base import Base as BasePage
from winipedia_pyside.utils.ui.widgets.media_player import MediaPlayer


class Player(BasePage):
    """Player page for the VideoVault application."""

    @abstractmethod
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start the playback.

        Args:
            path: The file path to start playback for.
            position: The position to start playback from in milliseconds.
        """

    def setup(self) -> None:
        """Setup the UI.

        Initializes the media player widget and adds it to the layout.
        """
        self.media_player = MediaPlayer(self.v_layout)

    def play_file_from_func(
        self,
        play_func: Callable[..., Any],
        path: Path,
        position: int = 0,
        **kwargs: Any,
    ) -> None:
        """Play a file using the specified function.

        Sets the current page to player and calls the provided play function
        with the given path and additional arguments.

        Args:
            play_func: The function to call for playing the file.
            path: The file path to play.
            position: The position to start playback from in milliseconds.
            **kwargs: Additional keyword arguments to pass to the play function.
        """
        # set current page to player
        self.set_current_page(self.__class__)
        # Stop current playback and clean up resources
        play_func(path=path, position=position, **kwargs)

    def play_file(self, path: Path, position: int = 0) -> None:
        """Play a regular video file.

        Args:
            path: The file path to play.
            position: The position to start playback from in milliseconds.
        """
        self.play_file_from_func(
            self.media_player.play_file, path=path, position=position
        )

    def play_encrypted_file(
        self, path: Path, aes_gcm: AESGCM, position: int = 0
    ) -> None:
        """Play an encrypted video file.

        Args:
            path: The encrypted file path to play.
            aes_gcm: The AES-GCM cipher instance for decryption.
            position: The position to start playback from in milliseconds.
        """
        self.play_file_from_func(
            self.media_player.play_encrypted_file,
            path=path,
            position=position,
            aes_gcm=aes_gcm,
        )
