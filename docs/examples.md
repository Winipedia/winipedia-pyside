# Examples

Practical examples demonstrating how to use Winipyside components.

## Basic Application

A minimal application with a single page:

```python
from PySide6.QtWidgets import QApplication, QLabel
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.base.base import Base as BasePage

class HomePage(BasePage):
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        label = QLabel("Hello, Winipyside!")
        self.v_layout.addWidget(label)
    
    def post_setup(self) -> None:
        pass

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

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
```

## Encrypted Video Player

A complete encrypted video player application:

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.player import Player

class VideoPlayerPage(Player):
    def __init__(self, base_window, *args, **kwargs):
        # Load encryption key
        self.aes_gcm = self.load_key()
        super().__init__(base_window, *args, **kwargs)
    
    def load_key(self) -> AESGCM:
        """Load or generate encryption key."""
        key_path = Path("encryption.key")
        if key_path.exists():
            with open(key_path, "rb") as f:
                key = f.read()
        else:
            key = AESGCM.generate_key(bit_length=256)
            with open(key_path, "wb") as f:
                f.write(key)
        return AESGCM(key)
    
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start playback of encrypted video."""
        self.play_encrypted_file(path, self.aes_gcm, position)
    
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        # Add file selection button
        select_btn = QPushButton("Select Video")
        select_btn.clicked.connect(self.select_video)
        self.h_layout.addWidget(select_btn)
    
    def post_setup(self) -> None:
        pass
    
    def select_video(self):
        """Open file dialog to select video."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            "",
            "Video Files (*.mp4 *.mkv *.avi)"
        )
        if path:
            self.start_playback(Path(path))

class VideoPlayerApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [VideoPlayerPage]
    
    @classmethod
    def get_start_page_cls(cls):
        return VideoPlayerPage
    
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        self.resize(1280, 720)
        self.setWindowTitle("Encrypted Video Player")
    
    def post_setup(self) -> None:
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = VideoPlayerApp()
    window.show()
    app.exec()
```

## Web Browser with Cookie Export

A web browser that can export cookies:

```python
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog
from PySide6.QtCore import QUrl
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.browser import Browser
import json

class BrowserPage(Browser):
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        # Add export cookies button
        export_btn = QPushButton("Export Cookies")
        export_btn.clicked.connect(self.export_cookies)
        self.h_layout.addWidget(export_btn)
        
        # Load default page
        self.browser.load(QUrl("https://example.com"))
    
    def post_setup(self) -> None:
        pass
    
    def export_cookies(self):
        """Export cookies to JSON file."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Cookies",
            "cookies.json",
            "JSON Files (*.json)"
        )
        if path:
            # Get all cookies
            all_cookies = {}
            for domain in self.get_all_domains():
                cookies = self.browser.get_domain_http_cookies(domain)
                all_cookies[domain] = [
                    {
                        "name": c.name,
                        "value": c.value,
                        "domain": c.domain,
                        "path": c.path,
                    }
                    for c in cookies
                ]
            
            # Save to file
            with open(path, "w") as f:
                json.dump(all_cookies, f, indent=2)
    
    def get_all_domains(self) -> list[str]:
        """Get all domains with cookies."""
        # This is a simplified version
        # In practice, you'd track domains as you browse
        return ["example.com"]

class BrowserApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [BrowserPage]
    
    @classmethod
    def get_start_page_cls(cls):
        return BrowserPage
    
    def pre_setup(self) -> None:
        pass
    
    def setup(self) -> None:
        self.resize(1280, 720)
        self.setWindowTitle("Web Browser")
    
    def post_setup(self) -> None:
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = BrowserApp()
    window.show()
    app.exec()
```

## See Also

- [Core Package](core.md)
- [UI Widgets](ui-widgets.md)
- [UI Pages](ui-pages.md)
- [UI Windows](ui-windows.md)

