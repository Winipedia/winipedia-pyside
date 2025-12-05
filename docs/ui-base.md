# UI Base Package

The `winipyside.src.ui.base` package provides the foundation framework for all UI components in Winipyside, including lifecycle management, navigation, and utility methods.

## Overview

The UI base package contains:

- **`Base`** - Abstract base class for all UI components
- **`QABCLoggingMeta`** - Custom metaclass combining ABC and Qt's metaclass

## Base Class

The `Base` class is the foundation for all UI components (widgets, pages, windows) in Winipyside. It provides a consistent lifecycle pattern and utility methods.

### Class Definition

```python
class Base(metaclass=QABCLoggingMeta):
    """Base UI class for a Qt application."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the base UI."""
        super().__init__(*args, **kwargs)
        self.base_setup()
        self.pre_setup()
        self.setup()
        self.post_setup()
```

### Key Features

- **4-phase lifecycle** with hooks for initialization
- **Automatic subclass discovery** across packages
- **Page navigation** methods for stacked layouts
- **SVG icon support** from resources
- **Display name generation** from class names
- **Custom metaclass** for proper ABC and Qt integration

## Lifecycle Hooks

All UI components follow a consistent 4-phase initialization pattern. Each phase has a specific purpose:

### 1. `base_setup()`

**Purpose:** Initialize core Qt components required for the UI to function.

**When to use:**
- Create Qt widgets (QVBoxLayout, QStackedWidget, etc.)
- Set window properties (title, size)
- Initialize Qt-specific attributes

**Example:**
```python
def base_setup(self) -> None:
    """Setup the base Qt object of the UI."""
    self.setWindowTitle(self.get_display_name())
    self.stack = QStackedWidget()
    self.setCentralWidget(self.stack)
```

### 2. `pre_setup()`

**Purpose:** Setup operations that must run before main setup.

**When to use:**
- Load configuration or settings
- Initialize data structures
- Setup connections that other components depend on
- Prepare resources

**Example:**
```python
def pre_setup(self) -> None:
    """Setup operations to run before main setup."""
    self.config = self.load_config()
    self.data_cache = {}
```

### 3. `setup()`

**Purpose:** Main UI initialization logic.

**When to use:**
- Add widgets to layouts
- Configure UI components
- Set up signal/slot connections
- Apply styling

**Example:**
```python
def setup(self) -> None:
    """Setup the main UI components."""
    self.resize(1280, 720)
    self.add_menu_bar()
    self.add_toolbar()
```

### 4. `post_setup()`

**Purpose:** Finalization after main setup is complete.

**When to use:**
- Final adjustments to UI
- Start background tasks
- Show initial dialogs
- Apply final state

**Example:**
```python
def post_setup(self) -> None:
    """Setup operations to run after main setup."""
    self.restore_window_state()
    self.check_for_updates()
```

## Methods

### Navigation Methods

#### `set_current_page(page_cls: type[BasePage]) -> None`

Set the current page in the stacked widget.

**Parameters:**
- `page_cls` (type[BasePage]): The page class to set as current

**Example:**
```python
from winipyside.src.ui.pages.browser import Browser

# Switch to browser page
self.set_current_page(Browser)
```

#### `get_page(page_cls: type[BasePage]) -> BasePage`

Get a page instance by its class.

**Parameters:**
- `page_cls` (type[BasePage]): The page class to retrieve

**Returns:**
- `BasePage`: The page instance

**Example:**
```python
browser_page = self.get_page(Browser)
browser_page.browser.load(QUrl("https://example.com"))
```

#### `get_stack() -> QStackedWidget`

Get the stacked widget containing all pages.

**Returns:**
- `QStackedWidget`: The stacked widget

**Example:**
```python
stack = self.get_stack()
current_index = stack.currentIndex()
```

### Utility Methods

#### `get_display_name() -> str` (classmethod)

Get the human-readable display name derived from the class name.

**Returns:**
- `str`: Display name with spaces between words

**Example:**
```python
class MyCustomWidget(Base, QWidget):
    pass

print(MyCustomWidget.get_display_name())  # "My Custom Widget"
```

#### `get_subclasses(package: ModuleType | None = None) -> list[type[Self]]` (classmethod)

Get all non-abstract subclasses of the UI component.

**Parameters:**
- `package` (ModuleType | None): Package to search in. If None, searches main package.

**Returns:**
- `list[type[Self]]`: Sorted list of all non-abstract subclasses

**Example:**
```python
from winipyside.src.ui.pages.base.base import Base as BasePage

# Get all page classes
all_pages = BasePage.get_subclasses()
for page_cls in all_pages:
    print(page_cls.__name__)
```

#### `get_svg_icon(name: str, color: str = "white") -> QIcon`

Load an SVG icon from resources.

**Parameters:**
- `name` (str): Icon name (without .svg extension)
- `color` (str): Icon color (default: "white")

**Returns:**
- `QIcon`: The loaded icon

**Example:**
```python
icon = self.get_svg_icon("play", color="blue")
button.setIcon(icon)
```

## QABCLoggingMeta

Custom metaclass that combines Python's ABC (Abstract Base Class) functionality with Qt's metaclass.

### Why It's Needed

Qt classes use a custom metaclass (`type(QObject)`), and Python's ABC uses its own metaclass. To use both together, we need a metaclass that inherits from both.

### Class Definition

```python
class QABCLoggingMeta(
    ABCLoggingMeta,  # From winiutils
    type(QObject),   # Qt's metaclass
):
    """Metaclass for Qt classes with ABC functionality."""
```

### Usage

The metaclass is automatically applied to the `Base` class, so all subclasses inherit it:

```python
from winipyside.src.ui.base.base import Base
from PySide6.QtWidgets import QWidget
from abc import abstractmethod

class MyWidget(Base, QWidget):
    @abstractmethod
    def custom_method(self) -> None:
        """This method must be implemented by subclasses."""
```

## Complete Example

Here's a complete example showing all lifecycle hooks and utility methods:

```python
from winipyside.src.ui.base.base import Base
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from abc import abstractmethod

class CustomWidget(Base, QWidget):
    """A custom widget demonstrating the Base class."""
    
    def base_setup(self) -> None:
        """Initialize Qt components."""
        # Create main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Set window title from class name
        self.setWindowTitle(self.get_display_name())  # "Custom Widget"
    
    def pre_setup(self) -> None:
        """Setup before main initialization."""
        # Load configuration
        self.config = {"theme": "dark", "font_size": 12}
        
        # Initialize data structures
        self.data = []
    
    def setup(self) -> None:
        """Main setup logic."""
        # Add widgets
        self.button = QPushButton("Click Me")
        self.layout.addWidget(self.button)
        
        # Connect signals
        self.button.clicked.connect(self.on_button_clicked)
        
        # Apply styling
        self.setStyleSheet("background-color: #2b2b2b;")
    
    def post_setup(self) -> None:
        """Finalization after setup."""
        # Show initial message
        print(f"{self.get_display_name()} initialized successfully")
    
    def on_button_clicked(self) -> None:
        """Handle button click."""
        print("Button clicked!")

# Usage
from PySide6.QtWidgets import QApplication

app = QApplication([])
widget = CustomWidget()
widget.show()
app.exec()
```

## Best Practices

### 1. Always Call Super

When overriding lifecycle methods, always call `super()` if the parent class has implementation:

```python
def base_setup(self) -> None:
    """Setup the base Qt object."""
    super().base_setup()  # Call parent implementation
    # Your custom setup
```

### 2. Keep Lifecycle Methods Focused

Each lifecycle method should have a clear, focused purpose:

```python
# Good - focused responsibilities
def base_setup(self) -> None:
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

def setup(self) -> None:
    self.add_widgets()
    self.connect_signals()

# Bad - mixing concerns
def base_setup(self) -> None:
    self.layout = QVBoxLayout()
    self.add_widgets()  # Should be in setup()
    self.load_config()  # Should be in pre_setup()
```

### 3. Use Abstract Methods for Required Implementation

Mark methods that subclasses must implement as abstract:

```python
from abc import abstractmethod

class CustomBase(Base, QWidget):
    @abstractmethod
    def load_data(self) -> None:
        """Load data - must be implemented by subclasses."""
```

### 4. Leverage Display Names

Use `get_display_name()` for consistent naming:

```python
def base_setup(self) -> None:
    # Automatically generates "My Custom Page" from "MyCustomPage"
    self.setWindowTitle(self.get_display_name())
```

### 5. Use Subclass Discovery for Plugins

Use `get_subclasses()` to discover and load plugins:

```python
# Get all page classes
all_pages = BasePage.get_subclasses()

# Create instances
for page_cls in all_pages:
    page = page_cls(parent=self)
```

## Common Patterns

### Pattern 1: Configuration Loading

```python
def pre_setup(self) -> None:
    """Load configuration before setup."""
    self.config = self.load_config()
    self.apply_theme(self.config.get("theme", "light"))
```

### Pattern 2: Lazy Widget Creation

```python
def setup(self) -> None:
    """Setup main UI."""
    # Create widgets on demand
    pass

def get_or_create_widget(self) -> QWidget:
    """Get widget, creating it if necessary."""
    if not hasattr(self, "_widget"):
        self._widget = QWidget()
    return self._widget
```

### Pattern 3: Signal Connection

```python
def setup(self) -> None:
    """Setup and connect signals."""
    self.button.clicked.connect(self.on_button_clicked)
    self.slider.valueChanged.connect(self.on_slider_changed)

def on_button_clicked(self) -> None:
    """Handle button click."""
    pass

def on_slider_changed(self, value: int) -> None:
    """Handle slider change."""
    pass
```

### Pattern 4: Resource Cleanup

```python
def closeEvent(self, event) -> None:
    """Clean up resources on close."""
    # Save state
    self.save_config()

    # Clean up resources
    if hasattr(self, "player"):
        self.player.stop()

    # Accept close event
    event.accept()
```

## See Also

- [UI Widgets](ui-widgets.md) - Widgets built on Base class
- [UI Pages](ui-pages.md) - Page components using Base
- [UI Windows](ui-windows.md) - Window framework using Base
- [Examples](examples.md) - More examples using Base class

