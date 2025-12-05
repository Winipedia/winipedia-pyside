# UI Windows Package

The `winipyside.src.ui.windows` package provides the main window framework for building multi-page Qt applications with QStackedWidget-based navigation.

## Overview

The windows package contains:

- **`windows.base.Base`** - Base window class (QMainWindow)

## Base Window

The base window class provides the foundation for multi-page applications.

### Class Definition

```python
class Base(BaseUI, QMainWindow):
    """Base window class for the application."""
    
    @classmethod
    @abstractmethod
    def get_all_page_classes(cls) -> list[type[BasePage]]:
        """Get all page classes.
        
        Returns:
            List of page classes to include in the application.
        """
    
    @classmethod
    @abstractmethod
    def get_start_page_cls(cls) -> type[BasePage]:
        """Get the start page class.
        
        Returns:
            The page class to display on startup.
        """
```

### Key Features

- **QStackedWidget integration**: Automatic page stacking and switching
- **Abstract page configuration**: Define pages via `get_all_page_classes()`
- **Start page selection**: Set initial page with `get_start_page_cls()`
- **Automatic page creation**: Pages are instantiated and added automatically
- **Window title**: Auto-generated from class name
- **Lifecycle hooks**: Inherits 4-phase initialization from BaseUI

### Attributes

- `stack` (QStackedWidget): The stacked widget containing all pages

### Abstract Methods

#### `get_all_page_classes() -> list[type[BasePage]]` (classmethod)

Get all page classes to include in the application.

**Returns:**
- `list[type[BasePage]]`: List of page classes

**Example:**
```python
@classmethod
def get_all_page_classes(cls):
    return [HomePage, SettingsPage, AboutPage]
```

#### `get_start_page_cls() -> type[BasePage]` (classmethod)

Get the page class to display on startup.

**Returns:**
- `type[BasePage]`: The start page class

**Example:**
```python
@classmethod
def get_start_page_cls(cls):
    return HomePage
```

### Methods

#### `make_pages() -> None`

Create and add all pages to the window.

**Automatically called in `base_setup()`**

#### `set_start_page() -> None`

Set the start page as the current page.

**Automatically called in `base_setup()`**

#### `add_page(page: BasePage) -> None`

Add a page to the stacked widget.

**Parameters:**
- `page` (BasePage): The page to add

**Note:** Usually called automatically by pages during initialization.

### Basic Example

```python
from PySide6.QtWidgets import QApplication
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.base.base import Base as BasePage
from PySide6.QtWidgets import QLabel

# Define a simple page
class HomePage(BasePage):
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        label = QLabel("Welcome to the Home Page")
        self.v_layout.addWidget(label)
    
    def post_setup(self) -> None:
        pass

# Define the main window
class MyApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [HomePage]
    
    @classmethod
    def get_start_page_cls(cls):
        return HomePage
    
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        self.resize(800, 600)
    
    def post_setup(self) -> None:
        pass

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
```

## Multi-Page Application

Here's a complete example with multiple pages and navigation:

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtCore import QUrl
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.base.base import Base as BasePage
from winipyside.src.ui.pages.player import Player
from winipyside.src.ui.pages.browser import Browser

# Home page
class HomePage(BasePage):
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        label = QLabel("Welcome! Choose a page from the menu.")
        self.v_layout.addWidget(label)
        
        # Add quick navigation buttons
        browser_btn = QPushButton("Open Browser")
        browser_btn.clicked.connect(lambda: self.base_window.set_current_page(BrowserPage))
        self.v_layout.addWidget(browser_btn)
        
        player_btn = QPushButton("Open Player")
        player_btn.clicked.connect(lambda: self.base_window.set_current_page(PlayerPage))
        self.v_layout.addWidget(player_btn)
    
    def post_setup(self) -> None:
        pass

# Browser page
class BrowserPage(Browser):
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        self.browser.load(QUrl("https://example.com"))
    
    def post_setup(self) -> None:
        pass

# Player page
class PlayerPage(Player):
    def __init__(self, base_window, *args, **kwargs):
        # Load encryption key
        key = AESGCM.generate_key(bit_length=256)
        self.aes_gcm = AESGCM(key)
        super().__init__(base_window, *args, **kwargs)
    
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start playback."""
        self.play_file(path, position)
    
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        pass
    
    def post_setup(self) -> None:
        pass

# Settings page
class SettingsPage(BasePage):
    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        label = QLabel("Settings")
        self.v_layout.addWidget(label)

        # Add settings controls
        theme_btn = QPushButton("Toggle Theme")
        self.v_layout.addWidget(theme_btn)

    def post_setup(self) -> None:
        pass

# Main window
class MyApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [HomePage, BrowserPage, PlayerPage, SettingsPage]

    @classmethod
    def get_start_page_cls(cls):
        return HomePage

    def pre_setup(self) -> None:
        """Setup before pages are created."""
        # Load configuration
        self.config = {"theme": "dark"}

    def setup(self) -> None:
        """Main window setup."""
        self.resize(1280, 720)
        self.setWindowTitle("My Application")

    def post_setup(self) -> None:
        """Finalization after setup."""
        # Apply theme
        if self.config["theme"] == "dark":
            self.setStyleSheet("background-color: #2b2b2b; color: white;")

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
```

## Best Practices

### Window Organization

1. **Keep window class focused**: The window should manage pages, not implement features
   ```python
   # Good
   class MyApp(BaseWindow):
       def setup(self) -> None:
           self.resize(1280, 720)
           self.setWindowTitle("My App")

   # Bad - too much logic in window
   class MyApp(BaseWindow):
       def setup(self) -> None:
           self.resize(1280, 720)
           self.load_database()
           self.start_background_tasks()
           self.check_for_updates()
   ```

2. **Use pre_setup for configuration**: Load config before pages are created
   ```python
   def pre_setup(self) -> None:
       self.config = self.load_config()
       self.apply_theme(self.config["theme"])
   ```

3. **Use post_setup for finalization**: Final adjustments after pages are ready
   ```python
   def post_setup(self) -> None:
       self.restore_window_state()
       self.check_for_updates()
   ```

### Page Management

1. **Define all pages in get_all_page_classes**:
   ```python
   @classmethod
   def get_all_page_classes(cls):
       return [HomePage, SettingsPage, AboutPage]
   ```

2. **Choose an appropriate start page**:
   ```python
   @classmethod
   def get_start_page_cls(cls):
       # Start with home page for most apps
       return HomePage
   ```

3. **Access pages when needed**:
   ```python
   # Get reference to a page
   settings_page = self.get_page(SettingsPage)
   settings_page.load_settings()
   ```

### State Management

1. **Save window state on close**:
   ```python
   def closeEvent(self, event):
       self.save_window_geometry()
       self.save_page_states()
       event.accept()
   ```

2. **Restore window state on startup**:
   ```python
   def setup(self) -> None:
       geometry = self.load_window_geometry()
       if geometry:
           self.restoreGeometry(geometry)
   ```

3. **Use shared data for inter-page communication**:
   ```python
   # In window class
   self.shared_data = {}

   # Pages can access via self.base_window.shared_data
   ```

## See Also

- [UI Base](ui-base.md) - Base class and lifecycle hooks
- [UI Pages](ui-pages.md) - Page components
- [Examples](examples.md) - Complete application examples

