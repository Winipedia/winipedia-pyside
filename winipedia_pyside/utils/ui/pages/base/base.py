"""Base page module.

This module contains the base page class for the VideoVault application.
"""

from functools import partial
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QMenu,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from winipedia_pyside.utils.ui.base.base import Base as BaseUI

if TYPE_CHECKING:
    from winipedia_pyside.utils.ui.windows.base.base import Base as BaseWindow


class Base(BaseUI, QWidget):
    """Base page class for the VideoVault application."""

    def __init__(self, base_window: "BaseWindow", *args: Any, **kwargs: Any) -> None:
        """Initialize the base page."""
        self.base_window = base_window
        super().__init__(*args, **kwargs)

    def base_setup(self) -> None:
        """Setup the base Qt object of the UI.

        Initializes the main vertical layout, adds a horizontal layout for the top row,
        and sets up the menu dropdown button.
        """
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        # add a horizontal layout for the top row
        self.h_layout = QHBoxLayout()
        self.v_layout.addLayout(self.h_layout)

        self.add_menu_dropdown_button()
        self.base_window.add_page(self)

    def add_menu_dropdown_button(self) -> None:
        """Add a dropdown menu that leads to each page.

        Creates a menu button with a dropdown containing actions for all available
        page subclasses. Each action connects to the set_current_page method.
        """
        self.menu_button = QPushButton("Menu")
        self.menu_button.setIcon(self.get_svg_icon("menu_icon"))
        self.menu_button.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.h_layout.addWidget(
            self.menu_button,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )
        self.menu_dropdown = QMenu(self.menu_button)
        self.menu_button.setMenu(self.menu_dropdown)

        for page_cls in self.base_window.get_all_page_classes():
            action = self.menu_dropdown.addAction(page_cls.get_display_name())
            action.triggered.connect(partial(self.set_current_page, page_cls))

    def add_to_page_button(
        self, to_page_cls: type["Base"], layout: QLayout
    ) -> QPushButton:
        """Add a button to go to the specified page.

        Args:
            to_page_cls: The page class to navigate to when button is clicked.
            layout: The layout to add the button to.

        Returns:
            The created QPushButton widget.
        """
        button = QPushButton(to_page_cls.get_display_name())

        # connect to open page on click
        button.clicked.connect(lambda: self.set_current_page(to_page_cls))

        # add to layout
        layout.addWidget(button)

        return button
