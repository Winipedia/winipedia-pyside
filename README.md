# winipedia_pyside
(Some parts are AI generated and may contain errors)

A comprehensive PySide6 utilities package providing enhanced UI components, encrypted file streaming, and a full-featured media player framework for building sophisticated Qt-based applications.

## Features

- **🎬 Full-Featured Media Player**: Complete media playback control with speed adjustment, volume control, progress tracking, and fullscreen support
- **🔐 Encrypted File Streaming**: AES-GCM encryption/decryption with transparent streaming for secure media playback
- **🎨 Reusable UI Components**: Pre-built widgets and base classes for rapid UI development
- **📱 Multi-Page Framework**: Abstract base classes for building multi-page applications with QStackedWidget
- **🔔 Toast Notifications**: Integrated notification system with auto-truncation
- **🎯 Type-Safe**: Full type hints with strict MyPy configuration
- **📚 Well-Documented**: Comprehensive docstrings following Google style guide

## Installation

### Requirements
- Python 3.12 - 3.13
- PySide6 >= 6.10.0

### Install from PyPI

```bash
pip install winipedia-pyside
```

## Quick Start

### Basic Media Player

```python
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from winipedia_pyside.ui.widgets.media_player import MediaPlayer

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Media Player")

# Create central widget and layout
central_widget = QWidget()
layout = QVBoxLayout(central_widget)
window.setCentralWidget(central_widget)

# Create media player
player = MediaPlayer(layout)

# Play a video file
player.play_file(Path("path/to/video.mp4"))

window.show()
app.exec()
```

### Encrypted Media Playback

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winipedia_pyside.ui.widgets.media_player import MediaPlayer

# Initialize cipher
key = b"your-32-byte-key-here-1234567890"  # 32 bytes for AES-256
aes_gcm = AESGCM(key)

# Create player and play encrypted file
player = MediaPlayer(layout)
player.play_encrypted_file(Path("path/to/encrypted_video.mp4"), aes_gcm)
```

### Show Notifications

```python
from pyqttoast import ToastIcon
from winipedia_pyside.ui.widgets.notification import Notification

# Show a notification
notification = Notification(
    title="Success",
    text="Operation completed successfully",
    icon=ToastIcon.SUCCESS,
    duration=5000  # milliseconds
)
notification.show()
```

### Create Custom UI Components

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from winipedia_pyside.ui.base.base import Base

class MyCustomWidget(Base, QWidget):
    def base_setup(self) -> None:
        """Initialize the Qt widget."""
        self.setWindowTitle("My Custom Widget")

    def pre_setup(self) -> None:
        """Pre-setup operations."""
        pass

    def setup(self) -> None:
        """Setup the main UI components."""
        layout = QVBoxLayout(self)
        label = QLabel("Hello, PySide6!")
        layout.addWidget(label)

    def post_setup(self) -> None:
        """Post-setup operations."""
        pass

# Use it
widget = MyCustomWidget()
widget.show()
```

## Core Modules

### `winipedia_pyside.core`

#### PyQIODevice
A Python-friendly wrapper around PySide6's QIODevice with enhanced functionality.

```python
from pathlib import Path
from winipedia_pyside.core.py_qiodevice import PyQFile

# Create a file device
file_device = PyQFile(Path("data.bin"))
file_device.open(QIODevice.ReadOnly)

# Read data
data = file_device.readData(1024)
file_device.close()
```

#### EncryptedPyQFile
Transparent AES-GCM encryption/decryption for file streaming.

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winipedia_pyside.core.py_qiodevice import EncryptedPyQFile

key = b"your-32-byte-key-here-1234567890"
aes_gcm = AESGCM(key)

# Create encrypted file device
encrypted_file = EncryptedPyQFile(Path("encrypted_data.bin"), aes_gcm)
encrypted_file.open(QIODevice.ReadOnly)

# Read decrypted data transparently
decrypted_data = encrypted_file.readData(1024)
encrypted_file.close()
```

### `winipedia_pyside.ui`

#### Base UI Class
Abstract base class for all UI components with lifecycle management.

**Lifecycle Methods:**
- `base_setup()`: Initialize core Qt objects
- `pre_setup()`: Pre-initialization operations
- `setup()`: Main UI initialization
- `post_setup()`: Post-initialization operations

**Utility Methods:**
- `get_display_name()`: Get human-readable class name
- `get_subclasses()`: Discover all subclasses
- `get_svg_icon()`: Load SVG icons
- `set_current_page()`: Switch pages in multi-page apps
- `get_page()`: Retrieve specific pages

#### MediaPlayer Widget
Full-featured media player with comprehensive controls.

**Features:**
- Play/pause control
- Speed adjustment (0.2x - 5x)
- Volume control
- Progress slider with seeking
- Fullscreen toggle
- Support for both regular and encrypted files

**Methods:**
- `play_file(path, position)`: Play a regular video file
- `play_encrypted_file(path, aes_gcm, position)`: Play encrypted video
- `play_video(io_device, source_url, position)`: Play from custom IO device
- `toggle_playback()`: Toggle play/pause
- `change_speed(speed)`: Change playback speed
- `toggle_fullscreen()`: Toggle fullscreen mode

#### Notification Widget
Toast notification system with auto-truncation.

```python
from winipedia_pyside.ui.widgets.notification import Notification
from pyqttoast import ToastIcon

notification = Notification(
    title="Title",
    text="Message text",
    icon=ToastIcon.INFORMATION,
    duration=10000
)
notification.show()
```

## Development
Comes with the winipedia_utils package and its testing framework.
Check out the [winipedia_utils](https://github.com/Winipedia/winipedia_utils) repository for more information on how to set up the development environment.

## License

MIT License - Copyright (c) 2025 Winipedia

See [LICENSE](LICENSE) file for details.
