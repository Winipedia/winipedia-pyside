# winipyside

(This project uses [pyrig](https://github.com/Winipedia/pyrig))

A comprehensive PySide6 utilities package providing reusable components for building Qt desktop applications. Features include encrypted file I/O with AES-GCM, a full-featured media player with support for encrypted video playback, an embedded web browser with cookie management, toast notifications, and a modular page-based UI framework. Built with strict type safety and production-ready CI/CD workflows for headless environments.

## Features

### Core (`winipyside.src.core`)

**Advanced QIODevice Wrappers for PySide6**

- **`PyQIODevice`**: Python-friendly wrapper around Qt's QIODevice with enhanced functionality
  - Provides clean Python interface to all QIODevice methods
  - Seamless integration with PySide6's I/O system
  - Support for sequential and random-access devices

- **`PyQFile`**: File-specific wrapper extending PyQIODevice
  - Simplified file operations with Path support
  - Compatible with Qt's media framework

- **`EncryptedPyQFile`**: Transparent AES-GCM encrypted file I/O
  - **Chunked encryption** for efficient streaming of large files (64KB cipher chunks)
  - **Position mapping** between encrypted and decrypted data for random access
  - **Authenticated encryption** using AES-GCM with 12-byte nonces and 16-byte tags
  - **Transparent decryption** - works seamlessly with Qt's QMediaPlayer for encrypted video playback
  - Static methods for standalone encryption/decryption operations
  - Secure random nonce generation per chunk
  - Associated authenticated data (AAD) for additional security

**Use Cases:**
- Play encrypted media files without temporary decryption
- Secure file storage with transparent access
- Streaming large encrypted files with minimal memory overhead

**Example:**

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import QUrl, QIODevice
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from winipyside.src.core.py_qiodevice import EncryptedPyQFile, PyQFile

# Generate or load your encryption key
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)

# Play an encrypted video file
video_path = Path("encrypted_video.mp4")
encrypted_file = EncryptedPyQFile(video_path, aes_gcm)
encrypted_file.open(QIODevice.OpenModeFlag.ReadOnly)

# Use with QMediaPlayer - decryption happens transparently
player = QMediaPlayer()
player.setAudioOutput(QAudioOutput())
player.setSourceDevice(encrypted_file, QUrl.fromLocalFile(video_path))
player.play()

# Or use PyQFile for regular (unencrypted) files
regular_file = PyQFile(Path("video.mp4"))
regular_file.open(QIODevice.OpenModeFlag.ReadOnly)
player.setSourceDevice(regular_file, QUrl.fromLocalFile("video.mp4"))
```

### UI Base (`winipyside.src.ui.base`)

**Foundation Framework for Qt Applications**

- **`Base`**: Abstract base class for all UI components with lifecycle management
  - **Lifecycle hooks**: `base_setup()`, `pre_setup()`, `setup()`, `post_setup()`
  - **Custom metaclass** (`QABCLoggingMeta`) combining ABC and Qt's metaclass for proper inheritance
  - **Dynamic subclass discovery**: Automatically find and instantiate UI components
  - **Page navigation**: Built-in methods for switching between pages in stacked layouts
  - **SVG icon support**: Easy loading of SVG icons from resources
  - **Display name generation**: Automatic human-readable names from class names

**Example:**

```python
from winipyside.src.ui.base.base import Base
from PySide6.QtWidgets import QWidget

class MyCustomWidget(Base, QWidget):
    def base_setup(self) -> None:
        # Initialize Qt components
        pass

    def pre_setup(self) -> None:
        # Setup before main initialization
        pass

    def setup(self) -> None:
        # Main setup logic
        self.setWindowTitle(self.get_display_name())  # "My Custom Widget"

    def post_setup(self) -> None:
        # Finalization after setup
        pass

# Discover all subclasses in your package
all_widgets = MyCustomWidget.get_subclasses()
```

### UI Widgets (`winipyside.src.ui.widgets`)

**Ready-to-Use Qt Widgets**

- **`Notification`**: Toast notification system using pyqttoast
  - **Auto-positioning**: Top-middle of screen
  - **Smart text truncation**: Automatically fits text to window width
  - **Customizable icons**: Information, warning, error, success
  - **Duration control**: Configurable display time

- **`ClickableWidget` / `ClickableVideoWidget`**: Click-enabled widgets
  - **Signal emission**: Emits `clicked` signal on left mouse button press
  - **Video widget variant**: Clickable QVideoWidget for media applications

- **`Browser`**: Full-featured embedded web browser
  - **Navigation controls**: Back, forward, address bar, go button
  - **Cookie management**: Automatic cookie tracking and conversion
  - **QNetworkCookie ↔ http.cookiejar.Cookie conversion**: Bridge Qt and Python cookie formats
  - **Domain-based cookie access**: Retrieve cookies by domain
  - **Auto-updates address bar**: Reflects current URL

- **`MediaPlayer`**: Comprehensive media player widget
  - **Playback controls**: Play/pause, speed adjustment (0.2x-5x), volume slider
  - **Progress control**: Seekable progress bar with throttled updates
  - **Fullscreen support**: Toggle fullscreen with automatic widget hiding
  - **Encrypted playback**: Native support for `EncryptedPyQFile`
  - **Clickable video**: Click to toggle control visibility
  - **Position resumption**: Resume playback from specific positions
  - **Smart resource management**: Proper cleanup of IO devices

**Example:**

```python
from winipyside.src.ui.widgets.notification import Notification
from winipyside.src.ui.widgets.media_player import MediaPlayer
from winipyside.src.ui.widgets.browser import Browser
from pyqttoast import ToastIcon
from PySide6.QtWidgets import QVBoxLayout
from pathlib import Path

# Show a notification
Notification(
    title="Download Complete",
    text="Your file has been downloaded successfully",
    icon=ToastIcon.SUCCESS,
    duration=5000
)

# Create a media player
layout = QVBoxLayout()
player = MediaPlayer(layout)
player.play_file(Path("video.mp4"))

# Or play encrypted file
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)
player.play_encrypted_file(Path("encrypted.mp4"), aes_gcm)

# Create a browser
browser = Browser(layout)
# Cookies are automatically tracked
cookies = browser.get_domain_http_cookies("example.com")
```

### UI Pages (`winipyside.src.ui.pages`)

**Page Components for Stacked Navigation**

- **`pages.base.Base`**: Base page class for application pages
  - **Menu dropdown**: Automatic navigation menu to all pages
  - **Page switching**: Built-in methods to navigate between pages
  - **Layout management**: Pre-configured vertical and horizontal layouts
  - **Window integration**: Automatic registration with parent window

- **`Player`**: Media player page
  - **Abstract playback method**: Customizable `start_playback()` for your use case
  - **Integrated MediaPlayer widget**: Full media player functionality
  - **Encrypted file support**: Play encrypted videos with `play_encrypted_file()`
  - **Auto page switching**: Automatically switches to player page on playback

- **`Browser`**: Web browser page
  - **Embedded browser widget**: Full web browsing capability
  - **Cookie access**: Retrieve cookies from browsing sessions

**Example:**

```python
from winipyside.src.ui.pages.player import Player
from winipyside.src.ui.pages.browser import Browser
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from pathlib import Path

class MyPlayerPage(Player):
    def start_playback(self, path: Path, position: int = 0) -> None:
        # Custom playback logic
        self.play_file(path, position)

class MyWindow(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [MyPlayerPage, Browser]

    @classmethod
    def get_start_page_cls(cls):
        return Browser

    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def post_setup(self) -> None:
        pass

# Pages automatically get menu navigation between each other
```

### UI Windows (`winipyside.src.ui.windows`)

**Main Window Framework**

- **`windows.base.Base`**: Base window class (QMainWindow)
  - **QStackedWidget integration**: Automatic page stacking and switching
  - **Abstract page configuration**: Define pages via `get_all_page_classes()`
  - **Start page selection**: Set initial page with `get_start_page_cls()`
  - **Automatic page creation**: Pages are instantiated and added automatically
  - **Window title**: Auto-generated from class name

**Example:**

```python
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.player import Player
from winipyside.src.ui.pages.browser import Browser
from PySide6.QtWidgets import QApplication

class MyApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [Player, Browser]

    @classmethod
    def get_start_page_cls(cls):
        return Browser

    def pre_setup(self) -> None:
        # Setup before pages are created
        pass

    def setup(self) -> None:
        # Main window setup
        self.resize(1280, 720)

    def post_setup(self) -> None:
        # Finalization
        pass

# Run the application
app = QApplication([])
window = MyApp()
window.show()
app.exec()
```


