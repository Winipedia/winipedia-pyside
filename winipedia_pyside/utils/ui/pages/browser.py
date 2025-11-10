"""Add downloads page module.

This module contains the add downloads page class for the VideoVault application.
"""

from winipedia_pyside.utils.ui.pages.base.base import Base as BasePage
from winipedia_pyside.utils.ui.widgets.browser import Browser as BrowserWidget


class Browser(BasePage):
    """Add downloads page for the VideoVault application."""

    def setup(self) -> None:
        """Setup the UI.

        Initializes the browser page by adding a browser widget to the layout.
        """
        self.add_brwoser()

    def add_brwoser(self) -> None:
        """Add a browser to surf the web.

        Creates and adds a BrowserWidget instance to the vertical layout,
        enabling web browsing functionality within the page.
        """
        self.browser = BrowserWidget(self.v_layout)
