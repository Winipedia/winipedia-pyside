"""Tests for Browser widget."""

from collections import defaultdict

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QLineEdit, QSizePolicy, QVBoxLayout, QWidget
from pytest_mock import MockFixture
from pytestqt.qtbot import QtBot
from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.ui.widgets.browser import Browser


@pytest.fixture
def parent_layout(qtbot: QtBot) -> QVBoxLayout:
    """Create parent layout for browser."""
    widget = QWidget()
    qtbot.addWidget(widget)
    return QVBoxLayout(widget)


class TestBrowser:
    """Test class for Browser."""

    @pytest.mark.skip
    def test___init__(self, parent_layout: QVBoxLayout, mocker: MockFixture) -> None:
        """Test method for __init__."""
        # Mock methods to avoid actual widget creation and network calls
        mock_make_widget = mocker.patch.object(Browser, "make_widget")
        mock_connect_signals = mocker.patch.object(Browser, "connect_signals")
        mock_load_first_url = mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)

        assert_with_msg(
            browser.parent_layout is parent_layout, "Parent layout should be set"
        )
        mock_make_widget.assert_called_once()
        mock_connect_signals.assert_called_once()
        mock_load_first_url.assert_called_once()

    @pytest.mark.skip
    def test_make_address_bar(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for make_address_bar."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        browser.browser_layout = QVBoxLayout()
        browser.make_address_bar()

        assert_with_msg(
            hasattr(browser, "address_bar_layout"),
            "Address bar layout should be created",
        )
        assert_with_msg(
            hasattr(browser, "back_button"), "Back button should be created"
        )
        assert_with_msg(
            hasattr(browser, "forward_button"), "Forward button should be created"
        )
        assert_with_msg(
            hasattr(browser, "address_bar"), "Address bar should be created"
        )
        assert_with_msg(hasattr(browser, "go_button"), "Go button should be created")
        assert_with_msg(
            hasattr(browser, "address_bar")
            and browser.address_bar.__class__.__name__ == "QLineEdit",
            "Address bar should be QLineEdit",
        )

    @pytest.mark.skip
    def test_navigate_to_url(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for navigate_to_url."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")
        mock_load = mocker.patch.object(Browser, "load")

        browser = Browser(parent_layout)
        browser.address_bar = QLineEdit()
        browser.address_bar.setText("https://example.com")

        browser.navigate_to_url()

        mock_load.assert_called_once()
        call_args = mock_load.call_args[0][0]
        assert_with_msg(
            call_args.__class__.__name__ == "QUrl", "Should call load with QUrl"
        )
        assert_with_msg(
            call_args.toString() == "https://example.com", "Should load correct URL"
        )

    @pytest.mark.skip
    def test_make_widget(self, qtbot: QtBot, mocker: MockFixture) -> None:
        """Test method for make_widget."""
        # Create a fresh parent layout for this test
        widget = QWidget()
        qtbot.addWidget(widget)
        parent_layout = QVBoxLayout(widget)

        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")
        # Don't mock these methods, let them run to test make_widget functionality

        browser = Browser(parent_layout)

        assert_with_msg(
            hasattr(browser, "browser_widget"), "Browser widget should be created"
        )
        assert_with_msg(
            hasattr(browser, "browser_layout"), "Browser layout should be created"
        )
        assert_with_msg(
            hasattr(browser, "browser_widget")
            and browser.browser_widget.__class__.__name__ == "QWidget",
            "Browser widget should be QWidget",
        )
        assert_with_msg(
            hasattr(browser, "browser_layout")
            and browser.browser_layout.__class__.__name__ == "QVBoxLayout",
            "Browser layout should be QVBoxLayout",
        )

    @pytest.mark.skip
    def test_set_size_policy(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for set_size_policy."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")
        mock_set_size_policy = mocker.patch.object(Browser, "setSizePolicy")

        browser = Browser(parent_layout)
        browser.set_size_policy()

        mock_set_size_policy.assert_called_once_with(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

    @pytest.mark.skip
    def test_connect_signals(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for connect_signals."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "load_first_url")
        mock_connect_load = mocker.patch.object(Browser, "connect_load_finished_signal")
        mock_connect_cookie = mocker.patch.object(
            Browser, "connect_on_cookie_added_signal"
        )

        browser = Browser(parent_layout)
        # Reset the call count since these methods are called during __init__
        mock_connect_load.reset_mock()
        mock_connect_cookie.reset_mock()

        browser.connect_signals()

        mock_connect_load.assert_called_once()
        mock_connect_cookie.assert_called_once()

    @pytest.mark.skip
    def test_connect_load_finished_signal(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for connect_load_finished_signal."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        # Test that the method runs without error (Qt signals can't be easily mocked)
        try:
            browser.connect_load_finished_signal()
            method_ran_successfully = True
        except (AttributeError, RuntimeError, TypeError):
            method_ran_successfully = False

        assert_with_msg(
            method_ran_successfully,
            "connect_load_finished_signal should run without error",
        )

    @pytest.mark.skip
    def test_on_load_finished(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for on_load_finished."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")
        mock_update_address = mocker.patch.object(Browser, "update_address_bar")
        mock_url = mocker.patch.object(
            Browser, "url", return_value=QUrl("https://test.com")
        )

        browser = Browser(parent_layout)
        browser.on_load_finished(_ok=True)

        mock_update_address.assert_called_once_with(mock_url.return_value)

    @pytest.mark.skip
    def test_update_address_bar(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for update_address_bar."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        browser.address_bar = QLineEdit()
        test_url = QUrl("https://example.com")

        browser.update_address_bar(test_url)

        assert_with_msg(
            browser.address_bar.text() == "https://example.com",
            f"Address bar should show URL, got {browser.address_bar.text()}",
        )

    @pytest.mark.skip
    def test_connect_on_cookie_added_signal(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for connect_on_cookie_added_signal."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        # Mock the page and profile chain
        mock_page = mocker.MagicMock()
        mock_profile = mocker.MagicMock()
        mock_cookie_store = mocker.MagicMock()
        mock_page.profile.return_value = mock_profile
        mock_profile.cookieStore.return_value = mock_cookie_store
        mocker.patch.object(Browser, "page", return_value=mock_page)

        browser = Browser(parent_layout)
        browser.connect_on_cookie_added_signal()

        assert_with_msg(hasattr(browser, "cookies"), "Cookies dict should be created")
        assert_with_msg(
            browser.cookies.__class__.__name__ == "defaultdict",
            "Cookies should be defaultdict",
        )
        mock_cookie_store.cookieAdded.connect.assert_called_once_with(
            browser.on_cookie_added
        )

    @pytest.mark.skip
    def test_on_cookie_added(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for on_cookie_added."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        browser.cookies = defaultdict(list)

        # Create mock cookie
        mock_cookie = mocker.MagicMock()
        mock_cookie.domain.return_value = "example.com"

        browser.on_cookie_added(mock_cookie)

        assert_with_msg(
            mock_cookie in browser.cookies["example.com"],
            "Cookie should be added to domain list",
        )

    @pytest.mark.skip
    def test_load_first_url(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for load_first_url."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mock_load = mocker.patch.object(Browser, "load")

        browser = Browser(parent_layout)
        # Reset the mock since load is called during __init__
        mock_load.reset_mock()
        browser.load_first_url()

        mock_load.assert_called_once()
        call_args = mock_load.call_args[0][0]
        assert_with_msg(
            call_args.__class__.__name__ == "QUrl", "Should call load with QUrl"
        )
        assert_with_msg(
            call_args.toString() == "https://www.google.com/",
            "Should load Google homepage",
        )

    @pytest.mark.skip
    def test_http_cookies(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for http_cookies."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        # Use type: ignore to bypass type checking for test purposes
        browser.cookies = {"example.com": [mocker.MagicMock()]}

        mock_convert = mocker.patch.object(
            browser, "qcookies_to_httpcookies", return_value=[mocker.MagicMock()]
        )

        result = browser.http_cookies

        assert_with_msg(result.__class__.__name__ == "dict", "Should return dict")
        assert_with_msg("example.com" in result, "Should contain domain key")
        mock_convert.assert_called_once()

    @pytest.mark.skip
    def test_qcookies_to_httpcookies(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for qcookies_to_httpcookies."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        mock_qcookie = mocker.MagicMock()
        mock_httpcookie = mocker.MagicMock()

        mock_convert = mocker.patch.object(
            browser, "qcookie_to_httpcookie", return_value=mock_httpcookie
        )

        result = browser.qcookies_to_httpcookies([mock_qcookie])

        assert_with_msg(result.__class__.__name__ == "list", "Should return list")
        assert_with_msg(len(result) == 1, "Should convert one cookie")
        assert_with_msg(result[0] is mock_httpcookie, "Should return converted cookie")
        mock_convert.assert_called_once_with(mock_qcookie)

    @pytest.mark.skip
    def test_qcookie_to_httpcookie(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for qcookie_to_httpcookie."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)

        # Create mock QNetworkCookie
        mock_qcookie = mocker.MagicMock()
        mock_qcookie.name.return_value.data.return_value = b"test_name"
        mock_qcookie.value.return_value.data.return_value = b"test_value"
        mock_qcookie.domain.return_value = "example.com"
        mock_qcookie.path.return_value = "/test"
        mock_qcookie.isSecure.return_value = True
        mock_qcookie.isHttpOnly.return_value = False
        mock_qcookie.expirationDate.return_value.isValid.return_value = False

        result = browser.qcookie_to_httpcookie(mock_qcookie)

        assert_with_msg(
            result.__class__.__name__ == "Cookie", "Should return Cookie instance"
        )
        assert_with_msg(result.name == "test_name", "Should set correct name")
        assert_with_msg(result.value == "test_value", "Should set correct value")
        assert_with_msg(result.domain == "example.com", "Should set correct domain")

    @pytest.mark.skip
    def test_get_domain_cookies(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for get_domain_cookies."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        test_cookies = [mocker.MagicMock(), mocker.MagicMock()]
        # Use type: ignore to bypass type checking for test purposes
        browser.cookies = {"example.com": test_cookies}

        result = browser.get_domain_cookies("example.com")

        assert_with_msg(result is test_cookies, "Should return cookies for domain")

    @pytest.mark.skip
    def test_get_domain_http_cookies(
        self, parent_layout: QVBoxLayout, mocker: MockFixture
    ) -> None:
        """Test method for get_domain_http_cookies."""
        mocker.patch.object(Browser, "make_widget")
        mocker.patch.object(Browser, "connect_signals")
        mocker.patch.object(Browser, "load_first_url")

        browser = Browser(parent_layout)
        test_qcookies = [mocker.MagicMock()]
        test_httpcookies = [mocker.MagicMock()]

        mock_get_domain = mocker.patch.object(
            browser, "get_domain_cookies", return_value=test_qcookies
        )
        mock_convert = mocker.patch.object(
            browser, "qcookies_to_httpcookies", return_value=test_httpcookies
        )

        result = browser.get_domain_http_cookies("example.com")

        assert_with_msg(result is test_httpcookies, "Should return converted cookies")
        mock_get_domain.assert_called_once_with("example.com")
        mock_convert.assert_called_once_with(test_qcookies)
