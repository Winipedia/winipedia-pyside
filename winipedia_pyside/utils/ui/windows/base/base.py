"""Base window module.

This module contains the base window class for the VideoVault application.
"""

from abc import abstractmethod

from PySide6.QtWidgets import QMainWindow, QStackedWidget

from winipedia_pyside.utils.ui.base.base import Base as BaseUI
from winipedia_pyside.utils.ui.pages.base.base import Base as BasePage


class Base(BaseUI, QMainWindow):
    """Base window class for the VideoVault application."""

    @classmethod
    @abstractmethod
    def get_all_page_classes(cls) -> list[type[BasePage]]:
        """Get all page classes."""

    @classmethod
    @abstractmethod
    def get_start_page_cls(cls) -> type[BasePage]:
        """Get the start page class."""

    def base_setup(self) -> None:
        """Get the Qt object of the UI."""
        self.setWindowTitle(self.get_display_name())

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.make_pages()

        self.set_start_page()

    def make_pages(self) -> None:
        """Get the pages to add to the window."""
        for page_cls in self.get_all_page_classes():
            page_cls(base_window=self)

    def set_start_page(self) -> None:
        """Set the start page."""
        self.set_current_page(self.get_start_page_cls())

    def add_page(self, page: BasePage) -> None:
        """Add the pages to the window."""
        self.stack.addWidget(page)
