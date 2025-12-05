# API Reference

Complete API reference for all Winipyside packages and classes.

## Core Package

### `winipyside.src.core.py_qiodevice`

#### PyQIODevice

```python
class PyQIODevice(QIODevice):
    """PySide6 QIODevice wrapper with enhanced functionality."""
    
    def __init__(self, q_device: QIODevice, *args: Any, **kwargs: Any) -> None
    def readData(self, maxlen: int) -> bytes
    def writeData(self, data: bytes) -> int
    def size() -> int
    def pos() -> int
    def seek(pos: int) -> bool
```

#### PyQFile

```python
class PyQFile(PyQIODevice):
    """QFile wrapper with enhanced Python integration."""
    
    def __init__(self, path: Path, *args: Any, **kwargs: Any) -> None
```

#### EncryptedPyQFile

```python
class EncryptedPyQFile(PyQFile):
    """Encrypted file wrapper with AES-GCM encryption."""
    
    # Constants
    NONCE_SIZE: int = 12
    TAG_SIZE: int = 16
    CIPHER_SIZE: int = 64 * 1024
    CHUNK_SIZE: int = 65564
    
    def __init__(self, path: Path, aes_gcm: AESGCM, *args: Any, **kwargs: Any) -> None
    def readData(self, maxlen: int) -> bytes
    def size() -> int
    def seek(pos: int) -> bool
    
    # Static methods
    @staticmethod
    def get_encrypted_pos(decrypted_pos: int) -> int
    
    @staticmethod
    def get_decrypted_pos(encrypted_pos: int) -> int
    
    @staticmethod
    def encrypt_file(input_path: Path, output_path: Path, aes_gcm: AESGCM) -> None
    
    @staticmethod
    def decrypt_file(input_path: Path, output_path: Path, aes_gcm: AESGCM) -> None
```

## UI Base Package

### `winipyside.src.ui.base.base`

#### QABCLoggingMeta

```python
class QABCLoggingMeta(ABCLoggingMeta, type(QObject)):
    """Metaclass for Qt classes with ABC functionality."""
```

#### Base

```python
class Base(metaclass=QABCLoggingMeta):
    """Base UI class for a Qt application."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None
    
    # Lifecycle methods (abstract)
    @abstractmethod
    def base_setup(self) -> None
    
    @abstractmethod
    def pre_setup(self) -> None
    
    @abstractmethod
    def setup(self) -> None
    
    @abstractmethod
    def post_setup(self) -> None
    
    # Utility methods
    @classmethod
    def get_display_name(cls) -> str
    
    @classmethod
    def get_subclasses(cls, package: ModuleType | None = None) -> list[type[Self]]
    
    def set_current_page(self, page_cls: type["BasePage"]) -> None
    def get_page(self, page_cls: type["BasePage"]) -> "BasePage"
    def get_stack(self) -> QStackedWidget
    def get_svg_icon(self, name: str, color: str = "white") -> QIcon
```

## UI Widgets Package

### `winipyside.src.ui.widgets.notification`

#### Notification

```python
class Notification(Toast):
    """Toast notification with auto-positioning and text truncation."""
    
    def __init__(
        self,
        title: str,
        text: str,
        duration: int = 10000,
        icon: ToastIcon = ToastIcon.INFORMATION,
        *args: Any,
        **kwargs: Any,
    ) -> None
```

### `winipyside.src.ui.widgets.clickable_widget`

#### ClickableWidget

```python
class ClickableWidget(QWidget):
    """A QWidget that emits a clicked signal."""
    
    clicked = Signal()
```

#### ClickableVideoWidget

```python
class ClickableVideoWidget(QVideoWidget):
    """A QVideoWidget that emits a clicked signal."""
    
    clicked = Signal()
```

### `winipyside.src.ui.widgets.browser`

#### Browser

```python
class Browser(QWebEngineView):
    """Embedded web browser with cookie management."""
    
    def __init__(self, layout: QLayout, *args: Any, **kwargs: Any) -> None
    
    def get_domain_cookies(self, domain: str) -> list[QNetworkCookie]
    def get_domain_http_cookies(self, domain: str) -> list[http.cookiejar.Cookie]
    
    @staticmethod
    def qcookie_to_httpcookie(qcookie: QNetworkCookie) -> http.cookiejar.Cookie
    
    @staticmethod
    def qcookies_to_httpcookies(qcookies: list[QNetworkCookie]) -> list[http.cookiejar.Cookie]
```

### `winipyside.src.ui.widgets.media_player`

#### MediaPlayer

```python
class MediaPlayer(QMediaPlayer):
    """Full-featured media player with controls."""
    
    def __init__(self, layout: QLayout, *args: Any, **kwargs: Any) -> None
    
    def play_file(self, path: Path, position: int = 0) -> None
    def play_encrypted_file(self, path: Path, aes_gcm: AESGCM, position: int = 0) -> None
    def play_video(self, io_device: PyQIODevice, url: QUrl, position: int = 0) -> None
    def stop_and_close_io_device(self) -> None
```

## UI Pages Package

### `winipyside.src.ui.pages.base.base`

#### Base

```python
class Base(BaseUI, QWidget):
    """Base page class for the application."""
    
    def __init__(self, base_window: "BaseWindow", *args: Any, **kwargs: Any) -> None
    
    # Attributes
    base_window: "BaseWindow"
    v_layout: QVBoxLayout
    h_layout: QHBoxLayout
    
    # Methods
    def add_menu_dropdown_button(self) -> None
    def add_to_page_button(self, page_cls: type["Base"], menu: QMenu) -> None
```

### `winipyside.src.ui.pages.player`

#### Player

```python
class Player(BasePage):
    """Media player page."""
    
    # Attributes
    player: MediaPlayer
    
    # Abstract method
    @abstractmethod
    def start_playback(self, path: Path, position: int = 0) -> None
    
    # Methods
    def play_file(self, path: Path, position: int = 0) -> None
    def play_encrypted_file(self, path: Path, aes_gcm: AESGCM, position: int = 0) -> None
    def play_file_from_func(self, func: Callable[[], Path], position: int = 0) -> None
```

### `winipyside.src.ui.pages.browser`

#### Browser

```python
class Browser(BasePage):
    """Web browser page."""
    
    # Attributes
    browser: BrowserWidget
```

## UI Windows Package

### `winipyside.src.ui.windows.base.base`

#### Base

```python
class Base(BaseUI, QMainWindow):
    """Base window class for the application."""
    
    # Attributes
    stack: QStackedWidget
    
    # Abstract methods
    @classmethod
    @abstractmethod
    def get_all_page_classes(cls) -> list[type[BasePage]]
    
    @classmethod
    @abstractmethod
    def get_start_page_cls(cls) -> type[BasePage]
    
    # Methods
    def make_pages(self) -> None
    def set_start_page(self) -> None
    def add_page(self, page: BasePage) -> None
```

## Type Aliases and Constants

### Encryption Constants

```python
NONCE_SIZE = 12      # 12-byte nonce for AES-GCM
TAG_SIZE = 16        # 16-byte authentication tag
CIPHER_SIZE = 64 * 1024  # 64KB cipher chunks
CHUNK_SIZE = 65564   # Total chunk size (nonce + cipher + tag)
```

## See Also

- [Core Package Documentation](core.md)
- [UI Base Documentation](ui-base.md)
- [UI Widgets Documentation](ui-widgets.md)
- [UI Pages Documentation](ui-pages.md)
- [UI Windows Documentation](ui-windows.md)

