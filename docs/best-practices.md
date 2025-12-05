# Best Practices

Design patterns and recommendations for building applications with Winipyside.

## Architecture

### Separation of Concerns

Keep your application well-organized by separating concerns:

```python
# Good - each page has a single responsibility
class VideoLibraryPage(BasePage):
    """Displays and manages video library."""
    pass

class VideoPlayerPage(Player):
    """Plays videos."""
    pass

class SettingsPage(BasePage):
    """Manages application settings."""
    pass

# Bad - one page doing everything
class MainPage(BasePage):
    """Does everything - library, playback, settings."""
    pass
```

### Use Lifecycle Hooks Appropriately

Each lifecycle hook has a specific purpose:

```python
class MyPage(BasePage):
    def base_setup(self) -> None:
        """Initialize Qt components only."""
        # Create layouts, widgets
        self.layout = QVBoxLayout()
    
    def pre_setup(self) -> None:
        """Load configuration and prepare data."""
        # Load config, initialize data structures
        self.config = self.load_config()
        self.data = []
    
    def setup(self) -> None:
        """Main UI setup."""
        # Add widgets, connect signals
        self.add_widgets()
        self.connect_signals()
    
    def post_setup(self) -> None:
        """Finalization."""
        # Apply final state, start background tasks
        self.restore_state()
```

## Security

### Key Management

Never hardcode encryption keys:

```python
# Bad - hardcoded key
key = b"my_secret_key_123"

# Good - load from secure storage
def load_key() -> bytes:
    key_path = Path.home() / ".myapp" / "encryption.key"
    if not key_path.exists():
        key = AESGCM.generate_key(bit_length=256)
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_bytes(key)
        # Set restrictive permissions
        key_path.chmod(0o600)
    return key_path.read_bytes()
```

### Secure File Handling

Always validate file paths and handle errors:

```python
def play_video(self, path: Path):
    """Play video with validation."""
    # Validate path
    if not path.exists():
        Notification(
            title="Error",
            text=f"File not found: {path}",
            icon=ToastIcon.ERROR
        )
        return
    
    # Check file size
    if path.stat().st_size > 10 * 1024 * 1024 * 1024:  # 10GB
        Notification(
            title="Warning",
            text="File is very large and may take time to load",
            icon=ToastIcon.WARNING
        )
    
    # Play video
    try:
        self.player.play_file(path)
    except Exception as e:
        Notification(
            title="Error",
            text=f"Failed to play video: {e}",
            icon=ToastIcon.ERROR
        )
```

## Performance

### Resource Management

Always clean up resources:

```python
class VideoPlayerPage(Player):
    def closeEvent(self, event):
        """Clean up on close."""
        # Stop playback and close files
        self.player.stop_and_close_io_device()
        
        # Save state
        self.save_playback_position()
        
        event.accept()
```

### Lazy Loading

Load resources only when needed:

```python
class VideoLibraryPage(BasePage):
    def setup(self) -> None:
        """Setup UI without loading videos."""
        self.video_list = QListWidget()
        self.v_layout.addWidget(self.video_list)
    
    def post_setup(self) -> None:
        """Load videos after UI is ready."""
        # Load in background to avoid blocking UI
        self.load_videos_async()
    
    def load_videos_async(self):
        """Load videos in background."""
        # Use QThread or similar for background loading
        pass
```

### Throttle Updates

Prevent excessive updates:

```python
from PySide6.QtCore import QTimer

class MyPage(BasePage):
    def setup(self) -> None:
        # Throttle slider updates
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)  # 100ms
        self.update_timer.timeout.connect(self.update_display)
        
        self.slider.valueChanged.connect(self.on_slider_changed)
    
    def on_slider_changed(self, value: int):
        """Handle slider change."""
        self.pending_value = value
        if not self.update_timer.isActive():
            self.update_timer.start()
    
    def update_display(self):
        """Update display with throttled value."""
        # Update UI with self.pending_value
        self.update_timer.stop()
```

## User Experience

### Provide Feedback

Always inform users about operations:

```python
def save_file(self, path: Path):
    """Save file with user feedback."""
    # Show progress
    Notification(
        title="Saving",
        text=f"Saving to {path.name}...",
        icon=ToastIcon.INFORMATION,
        duration=3000
    )
    
    try:
        # Perform save
        self.do_save(path)
        
        # Show success
        Notification(
            title="Success",
            text=f"Saved to {path.name}",
            icon=ToastIcon.SUCCESS,
            duration=3000
        )
    except Exception as e:
        # Show error
        Notification(
            title="Error",
            text=f"Failed to save: {e}",
            icon=ToastIcon.ERROR,
            duration=5000
        )
```

### Handle Errors Gracefully

Never let exceptions crash the application:

```python
def load_video(self, path: Path):
    """Load video with error handling."""
    try:
        self.player.play_file(path)
    except FileNotFoundError:
        Notification(
            title="Error",
            text="Video file not found",
            icon=ToastIcon.ERROR
        )
    except PermissionError:
        Notification(
            title="Error",
            text="Permission denied",
            icon=ToastIcon.ERROR
        )
    except Exception as e:
        Notification(
            title="Error",
            text=f"Unexpected error: {e}",
            icon=ToastIcon.ERROR
        )
        # Log error for debugging
        import logging
        logging.exception("Failed to load video")
```

### Save and Restore State

Preserve user preferences:

```python
class MyApp(BaseWindow):
    def pre_setup(self) -> None:
        """Load saved state."""
        self.config = self.load_config()
    
    def setup(self) -> None:
        """Apply saved state."""
        # Restore window geometry
        if "geometry" in self.config:
            self.restoreGeometry(self.config["geometry"])
        else:
            self.resize(1280, 720)
        
        # Restore theme
        theme = self.config.get("theme", "light")
        self.apply_theme(theme)
    
    def closeEvent(self, event):
        """Save state on close."""
        self.config["geometry"] = self.saveGeometry()
        self.save_config()
        event.accept()
    
    def load_config(self) -> dict:
        """Load configuration."""
        config_path = Path.home() / ".myapp" / "config.json"
        if config_path.exists():
            import json
            with open(config_path) as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save configuration."""
        config_path = Path.home() / ".myapp" / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=2)
```

## Testing

### Write Testable Code

Structure code for easy testing:

```python
# Good - testable
class VideoProcessor:
    def process_video(self, path: Path) -> Path:
        """Process video and return output path."""
        # Processing logic
        return output_path

class VideoPlayerPage(Player):
    def __init__(self, *args, **kwargs):
        self.processor = VideoProcessor()
        super().__init__(*args, **kwargs)
    
    def start_playback(self, path: Path, position: int = 0):
        processed_path = self.processor.process_video(path)
        self.play_file(processed_path, position)

# Bad - hard to test
class VideoPlayerPage(Player):
    def start_playback(self, path: Path, position: int = 0):
        # Processing logic mixed with UI logic
        # Hard to test without UI
        pass
```

## See Also

- [Examples](examples.md) - Practical examples
- [API Reference](api-reference.md) - Complete API documentation

