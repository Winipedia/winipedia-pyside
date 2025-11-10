"""Base UI module.

This module contains the base UI class for the VideoVault application.
"""

from abc import abstractmethod
from types import ModuleType
from typing import TYPE_CHECKING, Any, Self, cast

from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStackedWidget
from winipedia_utils.utils.data.structures.text.string import split_on_uppercase
from winipedia_utils.utils.modules.class_ import (
    get_all_nonabstract_subclasses,
)
from winipedia_utils.utils.modules.package import get_main_package, walk_package
from winipedia_utils.utils.oop.mixins.meta import ABCLoggingMeta
from winipedia_utils.utils.resources.svgs.svg import get_svg_path

# Avoid circular import
if TYPE_CHECKING:
    from winipedia_pyside.utils.ui.pages.base.base import Base as BasePage
    from winipedia_pyside.utils.ui.windows.base.base import Base as BaseWindow


class QABCLoggingMeta(
    ABCLoggingMeta,
    type(QObject),  # type: ignore[misc]
):
    """Metaclass for the QABCImplementationLoggingMixin."""


class Base(metaclass=QABCLoggingMeta):
    """Base UI class for a Qt application."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the base UI."""
        super().__init__(*args, **kwargs)
        self.base_setup()
        self.pre_setup()
        self.setup()
        self.post_setup()

    @abstractmethod
    def base_setup(self) -> None:
        """Setup the base Qt object of the UI.

        This method should initialize the core Qt components required
        for the UI to function properly.
        """

    @abstractmethod
    def setup(self) -> None:
        """Setup the main UI components.

        This method should contain the primary UI initialization logic.
        """

    @abstractmethod
    def pre_setup(self) -> None:
        """Setup operations to run before main setup.

        This method should contain any initialization that needs to happen
        before the main setup method is called.
        """

    @abstractmethod
    def post_setup(self) -> None:
        """Setup operations to run after main setup.

        This method should contain any finalization that needs to happen
        after the main setup method is called.
        """

    @classmethod
    def get_display_name(cls) -> str:
        """Get the display name of the UI.

        Returns:
            The human-readable display name derived from the class name.
        """
        return " ".join(split_on_uppercase(cls.__name__))

    @classmethod
    def get_subclasses(cls, package: ModuleType | None = None) -> list[type[Self]]:
        """Get all subclasses of the UI.

        Args:
            package: The package to search for subclasses in. If None,
                searches in the main package.

        Returns:
            A sorted list of all non-abstract subclasses.
        """
        if package is None:
            # find the main package
            package = get_main_package()

        _ = list(walk_package(package))

        children = get_all_nonabstract_subclasses(cls)
        return sorted(children, key=lambda cls: cls.__name__)

    def set_current_page(self, page_cls: type["BasePage"]) -> None:
        """Set the current page in the stack.

        Args:
            page_cls: The page class to set as current.
        """
        self.get_stack().setCurrentWidget(self.get_page(page_cls))

    def get_stack(self) -> QStackedWidget:
        """Get the stack widget of the window.

        Returns:
            The QStackedWidget containing all pages.
        """
        window = cast("BaseWindow", (getattr(self, "window", lambda: None)()))

        return window.stack

    def get_stack_pages(self) -> list["BasePage"]:
        """Get all pages from the stack.

        Returns:
            A list of all pages currently in the stack.
        """
        # Import here to avoid circular import

        stack = self.get_stack()
        # get all the pages
        return [cast("BasePage", stack.widget(i)) for i in range(stack.count())]

    def get_page[T: "BasePage"](self, page_cls: type[T]) -> T:
        """Get a specific page from the stack.

        Args:
            page_cls: The class of the page to retrieve.

        Returns:
            The page instance of the specified class.
        """
        page = next(
            page for page in self.get_stack_pages() if page.__class__ is page_cls
        )
        return cast("T", page)

    @classmethod
    def get_svg_icon(cls, svg_name: str, package: ModuleType | None = None) -> QIcon:
        """Get a QIcon for an SVG file.

        Args:
            svg_name: The name of the SVG file.
            package: The package to search for the SVG in. If None,
                searches in the main package.

        Returns:
            A QIcon created from the SVG file.
        """
        return QIcon(str(get_svg_path(svg_name, package=package)))

    @classmethod
    def get_page_static[T: "BasePage"](cls, page_cls: type[T]) -> T:
        """Get a page statically from the main window.

        Args:
            page_cls: The class of the page to retrieve.

        Returns:
            The page instance of the specified class from the main window.
        """
        from winipedia_pyside.utils.ui.windows.base.base import (  # noqa: PLC0415  bc of circular import
            Base as BaseWindow,
        )

        top_level_widgets = QApplication.topLevelWidgets()
        main_window = next(
            widget for widget in top_level_widgets if isinstance(widget, BaseWindow)
        )
        return main_window.get_page(page_cls)
