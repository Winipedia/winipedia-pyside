"""Browser module.

This module contains the browser class for the application.
"""

from collections import defaultdict
from http.cookiejar import Cookie
from typing import Any

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Browser(QWebEngineView):
    """Browser class that creates a simple ready to use browser and not just a view."""

    def __init__(self, parent_layout: QLayout, *args: Any, **kwargs: Any) -> None:
        """Initialize the browser.

        Args:
            parent_layout: The parent layout to add the browser widget to.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.parent_layout = parent_layout
        self.make_widget()
        self.connect_signals()
        self.load_first_url()

    def make_address_bar(self) -> None:
        """Make the address bar.

        Creates a horizontal layout containing back button, forward button,
        address input field, and go button for browser navigation.
        """
        self.address_bar_layout = QHBoxLayout()

        # Add back button
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon.fromTheme("go-previous"))
        self.back_button.setToolTip("Go back")
        self.back_button.clicked.connect(self.back)
        self.address_bar_layout.addWidget(self.back_button)

        # Add forward button
        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon.fromTheme("go-next"))
        self.forward_button.setToolTip("Go forward")
        self.forward_button.clicked.connect(self.forward)
        self.address_bar_layout.addWidget(self.forward_button)

        # Add address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL...")
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        self.address_bar_layout.addWidget(self.address_bar)

        # Add go button
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.navigate_to_url)
        self.address_bar_layout.addWidget(self.go_button)

        self.browser_layout.addLayout(self.address_bar_layout)

    def navigate_to_url(self) -> None:
        """Navigate to the URL entered in the address bar.

        Takes the URL from the address bar text field and loads it in the browser.
        """
        url = self.address_bar.text()
        self.load(QUrl(url))

    def make_widget(self) -> None:
        """Make the widget.

        Creates the main browser widget with vertical layout, sets size policy,
        creates the address bar, and adds components to the parent layout.
        """
        self.browser_widget = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_widget)
        self.set_size_policy()
        self.make_address_bar()
        self.browser_layout.addWidget(self)
        self.parent_layout.addWidget(self.browser_widget)

    def set_size_policy(self) -> None:
        """Set the size policy.

        Sets the browser to expand in both horizontal and vertical directions.
        """
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def connect_signals(self) -> None:
        """Connect the signals.

        Connects load finished signal and cookie added signal handlers.
        """
        self.connect_load_finished_signal()
        self.connect_on_cookie_added_signal()

    def connect_load_finished_signal(self) -> None:
        """Connect the load finished signal.

        Connects the loadStarted signal to the on_load_started handler.
        """
        self.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, _ok: bool) -> None:  # noqa: FBT001
        """Handle the load finished signal.

        Args:
            _ok: Boolean indicating if the load was successful (unused).
        """
        self.update_address_bar(self.url())

    def update_address_bar(self, url: QUrl) -> None:
        """Update the address bar with the current URL.

        Args:
            url: The QUrl to display in the address bar.
        """
        self.address_bar.setText(url.toString())

    def connect_on_cookie_added_signal(self) -> None:
        """Connect the on cookie added signal.

        Initializes the cookies dictionary and connects the cookieAdded signal
        to the on_cookie_added handler.
        """
        self.cookies: dict[str, list[QNetworkCookie]] = defaultdict(list)
        self.page().profile().cookieStore().cookieAdded.connect(self.on_cookie_added)

    def on_cookie_added(self, cookie: Any) -> None:
        """Handle the on cookie added signal.

        Args:
            cookie: The QNetworkCookie that was added.
        """
        self.cookies[cookie.domain()].append(cookie)

    def load_first_url(self) -> None:
        """Load the first URL.

        Loads Google's homepage as the initial page when the browser starts.
        """
        self.load(QUrl("https://www.google.com/"))

    @property
    def http_cookies(self) -> dict[str, list[Cookie]]:
        """Get the http cookies for all domains.

        Returns:
            Dictionary mapping domain names to lists of http.cookiejar.Cookie objects.
        """
        return {
            domain: self.qcookies_to_httpcookies(qcookies)
            for domain, qcookies in self.cookies.items()
        }

    def qcookies_to_httpcookies(self, qcookies: list[QNetworkCookie]) -> list[Cookie]:
        """Convert a list of QNetworkCookies to http.cookiejar.Cookie objects.

        Args:
            qcookies: List of QNetworkCookie objects to convert.

        Returns:
            List of converted http.cookiejar.Cookie objects.
        """
        return [self.qcookie_to_httpcookie(q_cookie) for q_cookie in qcookies]

    def qcookie_to_httpcookie(self, qcookie: QNetworkCookie) -> Cookie:
        """Convert a QNetworkCookie to a http.cookiejar.Cookie.

        Args:
            qcookie: The QNetworkCookie to convert.

        Returns:
            The converted http.cookiejar.Cookie object.
        """
        name = bytes(qcookie.name().data()).decode()
        value = bytes(qcookie.value().data()).decode()
        domain = qcookie.domain()
        path = qcookie.path() if qcookie.path() else "/"
        secure = qcookie.isSecure()
        expires = None
        if qcookie.expirationDate().isValid():
            expires = int(qcookie.expirationDate().toSecsSinceEpoch())
        rest = {"HttpOnly": str(qcookie.isHttpOnly())}

        return Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=bool(domain),
            domain_initial_dot=domain.startswith("."),
            path=path,
            path_specified=bool(path),
            secure=secure,
            expires=expires or None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=rest,
            rfc2109=False,
        )

    def get_domain_cookies(self, domain: str) -> list[QNetworkCookie]:
        """Get the cookies for the given domain.

        Args:
            domain: The domain to get cookies for.

        Returns:
            List of QNetworkCookie objects for the specified domain.
        """
        return self.cookies[domain]

    def get_domain_http_cookies(self, domain: str) -> list[Cookie]:
        """Get the http cookies for the given domain.

        Args:
            domain: The domain to get cookies for.

        Returns:
            List of http.cookiejar.Cookie objects for the specified domain.
        """
        cookies = self.get_domain_cookies(domain)
        return self.qcookies_to_httpcookies(cookies)
