# UI Widgets Package

The `winipyside.src.ui.widgets` package provides ready-to-use Qt widgets for common functionality including notifications, media playback, web browsing, and clickable widgets.

## Overview

The widgets package contains:

- **`Notification`** - Toast notification system
- **`Browser`** - Embedded web browser with cookie management
- **`MediaPlayer`** - Full-featured media player
- **`ClickableWidget`** - Click-enabled QWidget
- **`ClickableVideoWidget`** - Click-enabled QVideoWidget

## Notification

A toast notification system using pyqttoast with auto-positioning and smart text truncation.

### Class Definition

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
    ) -> None:
        """Initialize the notification."""
```

### Key Features

- **Auto-positioning**: Always appears at top-middle of screen
- **Smart text truncation**: Automatically fits text to half window width
- **Customizable icons**: Information, warning, error, success
- **Duration control**: Configurable display time in milliseconds
- **Non-blocking**: Doesn't interrupt user workflow

### Parameters

- `title` (str): Notification title
- `text` (str): Notification message (auto-truncated if too long)
- `duration` (int): Display duration in milliseconds (default: 10000)
- `icon` (ToastIcon): Icon type (default: INFORMATION)

### Example

```python
from winipyside.src.ui.widgets.notification import Notification
from pyqttoast import ToastIcon

# Information notification
Notification(
    title="Info",
    text="This is an information message",
    icon=ToastIcon.INFORMATION,
    duration=5000
)

# Success notification
Notification(
    title="Success",
    text="Operation completed successfully!",
    icon=ToastIcon.SUCCESS,
    duration=3000
)

# Warning notification
Notification(
    title="Warning",
    text="Please check your input",
    icon=ToastIcon.WARNING,
    duration=7000
)

# Error notification
Notification(
    title="Error",
    text="An error occurred while processing your request",
    icon=ToastIcon.ERROR,
    duration=10000
)
```

## ClickableWidget

A QWidget that emits a `clicked` signal when clicked with the left mouse button.

### Class Definition

```python
class ClickableWidget(QWidget):
    """A QWidget that emits a clicked signal."""
    
    clicked = Signal()  # Emitted when widget is clicked
```

### Key Features

- **Click detection**: Emits signal on left mouse button press
- **Qt Signal**: Standard Qt signal for easy connection
- **Lightweight**: Minimal overhead

### Example

```python
from winipyside.src.ui.widgets.clickable_widget import ClickableWidget
from PySide6.QtWidgets import QVBoxLayout, QLabel

# Create clickable widget
widget = ClickableWidget()
layout = QVBoxLayout()
widget.setLayout(layout)

label = QLabel("Click me!")
layout.addWidget(label)

# Connect to signal
widget.clicked.connect(lambda: print("Widget clicked!"))
```

## ClickableVideoWidget

A QVideoWidget that emits a `clicked` signal when clicked with the left mouse button.

### Class Definition

```python
class ClickableVideoWidget(QVideoWidget):
    """A QVideoWidget that emits a clicked signal."""
    
    clicked = Signal()  # Emitted when widget is clicked
```

### Key Features

- **Video widget**: Full QVideoWidget functionality
- **Click detection**: Emits signal on left mouse button press
- **Media integration**: Works with QMediaPlayer

### Example

```python
from winipyside.src.ui.widgets.clickable_widget import ClickableVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

# Create clickable video widget
video_widget = ClickableVideoWidget()

# Setup media player
player = QMediaPlayer()
player.setAudioOutput(QAudioOutput())
player.setVideoOutput(video_widget)

# Toggle play/pause on click
def toggle_playback():
    if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
        player.pause()
    else:
        player.play()

video_widget.clicked.connect(toggle_playback)
```

## Browser

An embedded Chromium-based web browser with navigation controls and cookie management.

### Class Definition

```python
class Browser(QWebEngineView):
    """Embedded web browser with cookie management."""
    
    def __init__(self, layout: QLayout, *args: Any, **kwargs: Any) -> None:
        """Initialize the browser."""
```

### Key Features

- **Full web browsing**: Chromium-based rendering engine
- **Navigation controls**: Back, forward, address bar, go button
- **Automatic cookie tracking**: Tracks cookies by domain
- **Cookie conversion**: QNetworkCookie ↔ http.cookiejar.Cookie
- **Domain-based access**: Retrieve cookies for specific domains
- **Auto-updating address bar**: Reflects current URL

### Methods

#### `get_domain_cookies(domain: str) -> list[QNetworkCookie]`

Get Qt cookies for a specific domain.

**Parameters:**
- `domain` (str): Domain name (e.g., "example.com")

**Returns:**
- `list[QNetworkCookie]`: List of Qt cookies

#### `get_domain_http_cookies(domain: str) -> list[http.cookiejar.Cookie]`

Get Python http.cookiejar cookies for a specific domain.

**Parameters:**
- `domain` (str): Domain name

**Returns:**
- `list[http.cookiejar.Cookie]`: List of Python cookies

#### Static Methods

##### `qcookie_to_httpcookie(qcookie: QNetworkCookie) -> http.cookiejar.Cookie`

Convert a Qt cookie to a Python cookie.

**Parameters:**
- `qcookie` (QNetworkCookie): Qt cookie

**Returns:**
- `http.cookiejar.Cookie`: Python cookie

##### `qcookies_to_httpcookies(qcookies: list[QNetworkCookie]) -> list[http.cookiejar.Cookie]`

Convert a list of Qt cookies to Python cookies.

**Parameters:**
- `qcookies` (list[QNetworkCookie]): List of Qt cookies

**Returns:**
- `list[http.cookiejar.Cookie]`: List of Python cookies

### Browser Cookie Management

**Complete Example:**

```python
from winipyside.src.ui.widgets.browser import Browser
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl

# Create application
app = QApplication([])
window = QMainWindow()
widget = QWidget()
layout = QVBoxLayout()
widget.setLayout(layout)
window.setCentralWidget(widget)

# Create browser
browser = Browser(layout)

# Navigate to a website
browser.load(QUrl("https://example.com"))

# Later, retrieve cookies
qt_cookies = browser.get_domain_cookies("example.com")
python_cookies = browser.get_domain_http_cookies("example.com")

# Use Python cookies with requests
import requests
session = requests.Session()
for cookie in python_cookies:
    session.cookies.set_cookie(cookie)

window.show()
app.exec()
```

## MediaPlayer

A comprehensive media player widget with playback controls, speed adjustment, volume control, and encrypted file support.

### Class Definition

```python
class MediaPlayer(QMediaPlayer):
    """Full-featured media player with controls."""

    def __init__(self, layout: QLayout, *args: Any, **kwargs: Any) -> None:
        """Initialize the media player."""
```

### Key Features

- **Playback controls**: Play/pause button
- **Speed control**: Adjustable playback speed (0.2x to 5.0x)
- **Volume control**: Volume slider with mute
- **Progress bar**: Seekable progress bar with throttled updates
- **Fullscreen mode**: Toggle fullscreen with automatic UI hiding
- **Encrypted playback**: Native support for EncryptedPyQFile
- **Position resumption**: Resume playback from specific positions
- **Clickable video**: Click video to toggle control visibility
- **Resource management**: Proper cleanup of IO devices

### Methods

#### `play_file(path: Path, position: int = 0) -> None`

Play a regular (unencrypted) file.

**Parameters:**
- `path` (Path): Path to media file
- `position` (int): Starting position in milliseconds (default: 0)

**Example:**
```python
from pathlib import Path
from winipyside.src.ui.widgets.media_player import MediaPlayer
from PySide6.QtWidgets import QVBoxLayout

layout = QVBoxLayout()
player = MediaPlayer(layout)

# Play from beginning
player.play_file(Path("video.mp4"))

# Resume from 30 seconds
player.play_file(Path("video.mp4"), position=30000)
```

#### `play_encrypted_file(path: Path, aes_gcm: AESGCM, position: int = 0) -> None`

Play an encrypted file.

**Parameters:**
- `path` (Path): Path to encrypted media file
- `aes_gcm` (AESGCM): AES-GCM cipher instance
- `position` (int): Starting position in milliseconds (default: 0)

**Example:**
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Load encryption key
with open("encryption.key", "rb") as f:
    key = f.read()
aes_gcm = AESGCM(key)

# Play encrypted file
player.play_encrypted_file(Path("encrypted_video.mp4"), aes_gcm)
```

#### `play_video(io_device: PyQIODevice, url: QUrl, position: int = 0) -> None`

Play from a custom IO device.

**Parameters:**
- `io_device` (PyQIODevice): IO device to read from
- `url` (QUrl): URL for media source
- `position` (int): Starting position in milliseconds (default: 0)

#### `stop_and_close_io_device() -> None`

Stop playback and close the IO device.

**Example:**
```python
player.stop_and_close_io_device()
```

### Controls

The MediaPlayer automatically creates and manages the following controls:

#### Playback Control
- **Play/Pause button**: Toggle playback state
- **Auto-updates**: Button icon changes based on playback state

#### Speed Control
- **Speed slider**: Adjust playback speed from 0.2x to 5.0x
- **Speed label**: Displays current speed (e.g., "1.0x")
- **Logarithmic scale**: Natural feel for speed adjustment

#### Volume Control
- **Volume slider**: Adjust volume from 0% to 100%
- **Volume label**: Displays current volume percentage

#### Progress Control
- **Progress slider**: Seek to any position in the media
- **Throttled updates**: Updates every 100ms to prevent lag
- **Time display**: Shows current position and total duration

#### Fullscreen Control
- **Fullscreen button**: Toggle fullscreen mode
- **Auto-hide controls**: Controls hide in fullscreen, show on mouse move
- **Exit fullscreen**: Press Escape or click fullscreen button

### Complete Example

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from winipyside.src.ui.widgets.media_player import MediaPlayer

# Create application
app = QApplication([])
window = QMainWindow()
widget = QWidget()
layout = QVBoxLayout()
widget.setLayout(layout)
window.setCentralWidget(widget)

# Create media player
player = MediaPlayer(layout)

# Load encryption key
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)

# Play encrypted video
player.play_encrypted_file(Path("encrypted_video.mp4"), aes_gcm)

# Or play regular video
# player.play_file(Path("video.mp4"))

window.resize(1280, 720)
window.show()
app.exec()
```

## Best Practices

### Notification Best Practices

1. **Use appropriate icons** for message types:
   ```python
   # Success
   Notification(title="Success", text="...", icon=ToastIcon.SUCCESS)

   # Error
   Notification(title="Error", text="...", icon=ToastIcon.ERROR)
   ```

2. **Keep messages concise**: Text is auto-truncated, but shorter is better

3. **Adjust duration** based on message importance:
   ```python
   # Quick info - 3 seconds
   Notification(title="Info", text="...", duration=3000)

   # Important warning - 10 seconds
   Notification(title="Warning", text="...", duration=10000)
   ```

### Browser Best Practices

1. **Handle cookie expiration**:
   ```python
   cookies = browser.get_domain_http_cookies("example.com")
   valid_cookies = [c for c in cookies if not c.is_expired()]
   ```

2. **Clear cookies when needed**:
   ```python
   profile = browser.page().profile()
   profile.cookieStore().deleteAllCookies()
   ```

3. **Use cookie conversion** for requests integration:
   ```python
   python_cookies = browser.get_domain_http_cookies("example.com")
   session = requests.Session()
   for cookie in python_cookies:
       session.cookies.set_cookie(cookie)
   ```

### MediaPlayer Best Practices

1. **Always clean up resources**:
   ```python
   def closeEvent(self, event):
       self.player.stop_and_close_io_device()
       event.accept()
   ```

2. **Handle playback errors**:
   ```python
   player.errorOccurred.connect(lambda error: print(f"Error: {error}"))
   ```

3. **Save and restore position**:
   ```python
   # Save position
   position = player.position()

   # Restore later
   player.play_file(path, position=position)
   ```

4. **Use encrypted files** for sensitive content:
   ```python
   # Always use EncryptedPyQFile for sensitive videos
   player.play_encrypted_file(path, aes_gcm)
   ```

## See Also

- [Core Package](core.md) - EncryptedPyQFile for media player
- [UI Pages](ui-pages.md) - Player and Browser pages
- [Examples](examples.md) - More widget examples

