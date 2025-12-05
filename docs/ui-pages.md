# UI Pages Package

The `winipyside.src.ui.pages` package provides page components for building multi-page applications with QStackedWidget-based navigation.

## Overview

The pages package contains:

- **`pages.base.Base`** - Base page class for all pages
- **`Player`** - Media player page
- **`Browser`** - Web browser page

## Base Page

The base page class provides the foundation for all pages in a multi-page application.

### Class Definition

```python
class Base(BaseUI, QWidget):
    """Base page class for the application."""
    
    def __init__(self, base_window: "BaseWindow", *args: Any, **kwargs: Any) -> None:
        """Initialize the base page.
        
        Args:
            base_window: The parent window containing this page.
        """
```

### Key Features

- **Automatic registration**: Pages register themselves with the parent window
- **Menu dropdown**: Navigation menu to switch between pages
- **Pre-configured layouts**: Vertical and horizontal layouts ready to use
- **Window reference**: Access to parent window for navigation
- **Lifecycle hooks**: Inherits 4-phase initialization from BaseUI

### Attributes

- `base_window` (BaseWindow): Reference to the parent window
- `v_layout` (QVBoxLayout): Main vertical layout
- `h_layout` (QHBoxLayout): Top horizontal layout for controls

### Methods

#### `add_menu_dropdown_button() -> None`

Add a dropdown menu button for page navigation.

**Automatically called in `base_setup()`**

#### `add_to_page_button(page_cls: type["Base"], menu: QMenu) -> None`

Add a button to the menu for navigating to a specific page.

**Parameters:**
- `page_cls` (type[Base]): The page class to navigate to
- `menu` (QMenu): The menu to add the button to

### Example

```python
from winipyside.src.ui.pages.base.base import Base as BasePage
from PySide6.QtWidgets import QLabel, QPushButton

class CustomPage(BasePage):
    def pre_setup(self) -> None:
        """Setup before main initialization."""
        pass
    
    def setup(self) -> None:
        """Main setup logic."""
        # Add widgets to the vertical layout
        label = QLabel("Welcome to Custom Page")
        self.v_layout.addWidget(label)
        
        button = QPushButton("Click Me")
        button.clicked.connect(self.on_button_clicked)
        self.v_layout.addWidget(button)
    
    def post_setup(self) -> None:
        """Finalization after setup."""
        pass
    
    def on_button_clicked(self) -> None:
        """Handle button click."""
        print("Button clicked!")
```

## Player Page

A page with an integrated media player for playing videos.

### Class Definition

```python
class Player(BasePage):
    """Media player page."""
    
    @abstractmethod
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start playback - must be implemented by subclasses.
        
        Args:
            path: Path to media file.
            position: Starting position in milliseconds.
        """
```

### Key Features

- **Integrated MediaPlayer**: Full-featured media player widget
- **Abstract playback method**: Customize playback behavior
- **Encrypted file support**: Play encrypted videos
- **Auto page switching**: Automatically switches to player page on playback
- **Position resumption**: Resume from specific positions

### Attributes

- `player` (MediaPlayer): The media player widget

### Methods

#### `start_playback(path: Path, position: int = 0) -> None` (abstract)

Start playback of a media file. Must be implemented by subclasses.

**Parameters:**
- `path` (Path): Path to media file
- `position` (int): Starting position in milliseconds (default: 0)

#### `play_file(path: Path, position: int = 0) -> None`

Play a regular (unencrypted) file.

**Parameters:**
- `path` (Path): Path to media file
- `position` (int): Starting position in milliseconds (default: 0)

#### `play_encrypted_file(path: Path, aes_gcm: AESGCM, position: int = 0) -> None`

Play an encrypted file.

**Parameters:**
- `path` (Path): Path to encrypted media file
- `aes_gcm` (AESGCM): AES-GCM cipher instance
- `position` (int): Starting position in milliseconds (default: 0)

#### `play_file_from_func(func: Callable[[], Path], position: int = 0) -> None`

Play a file from a function that returns the path.

**Parameters:**
- `func` (Callable[[], Path]): Function that returns the file path
- `position` (int): Starting position in milliseconds (default: 0)

### Example

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winipyside.src.ui.pages.player import Player

class MyPlayerPage(Player):
    def __init__(self, base_window, *args, **kwargs):
        self.aes_gcm = self.load_encryption_key()
        super().__init__(base_window, *args, **kwargs)
    
    def load_encryption_key(self) -> AESGCM:
        """Load encryption key."""
        with open("encryption.key", "rb") as f:
            key = f.read()
        return AESGCM(key)
    
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start playback of encrypted video."""
        # Check if file is encrypted
        if path.suffix == ".encrypted":
            self.play_encrypted_file(path, self.aes_gcm, position)
        else:
            self.play_file(path, position)
    
    def pre_setup(self) -> None:
        """Setup before main initialization."""
        pass
    
    def setup(self) -> None:
        """Main setup logic."""
        # Player widget is automatically created
        # Add custom controls if needed
        pass
    
    def post_setup(self) -> None:
        """Finalization after setup."""
        pass
```

## Browser Page

A page with an embedded web browser.

### Class Definition

```python
class Browser(BasePage):
    """Web browser page."""
```

### Key Features

- **Integrated Browser**: Full-featured web browser widget
- **Cookie access**: Retrieve cookies from browsing sessions
- **Navigation controls**: Built into the browser widget
- **Simple setup**: Minimal configuration required

### Attributes

- `browser` (Browser): The browser widget

### Example

```python
from winipyside.src.ui.pages.browser import Browser
from PySide6.QtCore import QUrl

class MyBrowserPage(Browser):
    def pre_setup(self) -> None:
        """Setup before main initialization."""
        pass
    
    def setup(self) -> None:
        """Main setup logic."""
        # Browser widget is automatically created
        # Load a default page
        self.browser.load(QUrl("https://example.com"))
    
    def post_setup(self) -> None:
        """Finalization after setup."""
        # Access cookies if needed
        cookies = self.browser.get_domain_http_cookies("example.com")
        print(f"Found {len(cookies)} cookies")
```

## Multi-Page Application

Here's a complete example of a multi-page application using all page types:

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtWidgets import QApplication
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.player import Player
from winipyside.src.ui.pages.browser import Browser

# Custom player page
class MyPlayerPage(Player):
    def __init__(self, base_window, *args, **kwargs):
        # Load encryption key
        with open("encryption.key", "rb") as f:
            key = f.read()
        self.aes_gcm = AESGCM(key)
        super().__init__(base_window, *args, **kwargs)

    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start playback."""
        if path.suffix == ".encrypted":
            self.play_encrypted_file(path, self.aes_gcm, position)
        else:
            self.play_file(path, position)

    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def post_setup(self) -> None:
        pass

# Custom browser page
class MyBrowserPage(Browser):
    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        # Load default page
        from PySide6.QtCore import QUrl
        self.browser.load(QUrl("https://example.com"))

    def post_setup(self) -> None:
        pass

# Main window
class MyApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [MyBrowserPage, MyPlayerPage]

    @classmethod
    def get_start_page_cls(cls):
        return MyBrowserPage

    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        self.resize(1280, 720)

    def post_setup(self) -> None:
        pass

# Run application
if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
```

## Best Practices

### Page Organization

1. **One page per feature**: Each page should represent a distinct feature or view
   ```python
   # Good
   class VideoLibraryPage(BasePage): pass
   class SettingsPage(BasePage): pass
   class AboutPage(BasePage): pass

   # Bad - too many features in one page
   class EverythingPage(BasePage): pass
   ```

2. **Use descriptive names**: Page class names should clearly indicate their purpose
   ```python
   # Good
   class VideoPlayerPage(Player): pass
   class WebBrowserPage(Browser): pass

   # Bad
   class Page1(Player): pass
   class MyPage(Browser): pass
   ```

### Player Page Best Practices

1. **Implement start_playback**: Always implement the abstract method
   ```python
   def start_playback(self, path: Path, position: int = 0) -> None:
       """Start playback."""
       # Your implementation
   ```

2. **Handle both encrypted and regular files**:
   ```python
   def start_playback(self, path: Path, position: int = 0) -> None:
       if self.is_encrypted(path):
           self.play_encrypted_file(path, self.aes_gcm, position)
       else:
           self.play_file(path, position)
   ```

3. **Save playback position**:
   ```python
   def closeEvent(self, event):
       position = self.player.position()
       self.save_position(self.current_file, position)
       event.accept()
   ```

### Browser Page Best Practices

1. **Set a default URL**:
   ```python
   def setup(self) -> None:
       self.browser.load(QUrl("https://example.com"))
   ```

2. **Handle navigation events**:
   ```python
   def setup(self) -> None:
       self.browser.urlChanged.connect(self.on_url_changed)

   def on_url_changed(self, url):
       print(f"Navigated to: {url.toString()}")
   ```

3. **Manage cookies**:
   ```python
   def get_session_cookies(self, domain: str):
       """Get cookies for a domain."""
       return self.browser.get_domain_http_cookies(domain)
   ```

### Navigation Best Practices

1. **Use set_current_page for navigation**:
   ```python
   # Navigate to player page
   self.base_window.set_current_page(MyPlayerPage)
   ```

2. **Access other pages**:
   ```python
   # Get reference to another page
   player_page = self.base_window.get_page(MyPlayerPage)
   player_page.start_playback(Path("video.mp4"))
   ```

3. **Communicate between pages**:
   ```python
   # In browser page
   def on_video_link_clicked(self, url):
       player_page = self.base_window.get_page(MyPlayerPage)
       player_page.start_playback(self.download_video(url))
       self.base_window.set_current_page(MyPlayerPage)
   ```

## See Also

- [UI Base](ui-base.md) - Base class and lifecycle hooks
- [UI Widgets](ui-widgets.md) - Browser and MediaPlayer widgets
- [UI Windows](ui-windows.md) - Window framework for pages
- [Examples](examples.md) - More page examples

