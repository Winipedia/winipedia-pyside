# Core Package

The `winipyside.src.core` package provides advanced QIODevice wrappers for PySide6, including transparent AES-GCM encryption for files and media playback.

## Overview

The core package contains three main classes:

- **`PyQIODevice`** - Python-friendly wrapper around Qt's QIODevice
- **`PyQFile`** - File-specific wrapper with Path support
- **`EncryptedPyQFile`** - Transparent AES-GCM encrypted file I/O

## PyQIODevice

A Python-friendly wrapper around PySide6's QIODevice that provides enhanced functionality and easier integration with Python code.

### Class Definition

```python
class PyQIODevice(QIODevice):
    """PySide6 QIODevice wrapper with enhanced functionality."""
    
    def __init__(self, q_device: QIODevice, *args: Any, **kwargs: Any) -> None:
        """Initialize the PyQIODevice wrapper.
        
        Args:
            q_device: The QIODevice instance to wrap.
        """
```

### Key Features

- Wraps any QIODevice instance
- Provides Python-friendly interface
- Maintains all original QIODevice functionality
- Seamless integration with PySide6's I/O system

### Methods

#### `readData(maxlen: int) -> bytes`

Read data from the device.

**Parameters:**
- `maxlen` (int): Maximum number of bytes to read

**Returns:**
- `bytes`: The data read from the device

#### `writeData(data: bytes) -> int`

Write data to the device.

**Parameters:**
- `data` (bytes): The data to write

**Returns:**
- `int`: Number of bytes written

#### `size() -> int`

Get the size of the device.

**Returns:**
- `int`: Size in bytes

#### `pos() -> int`

Get the current position in the device.

**Returns:**
- `int`: Current position in bytes

#### `seek(pos: int) -> bool`

Seek to a specific position.

**Parameters:**
- `pos` (int): Position to seek to

**Returns:**
- `bool`: True if successful

### Example

```python
from PySide6.QtCore import QFile, QIODevice
from winipyside.src.core.py_qiodevice import PyQIODevice

# Wrap a QFile
qfile = QFile("example.txt")
device = PyQIODevice(qfile)
device.open(QIODevice.OpenModeFlag.ReadOnly)

# Read data
data = device.readData(1024)
print(data)

device.close()
```

## PyQFile

A file-specific wrapper extending PyQIODevice with simplified file operations and Path support.

### Class Definition

```python
class PyQFile(PyQIODevice):
    """QFile wrapper with enhanced Python integration."""
    
    def __init__(self, path: Path, *args: Any, **kwargs: Any) -> None:
        """Initialize the PyQFile with a file path.
        
        Args:
            path: The file path to open.
        """
```

### Key Features

- Accepts `pathlib.Path` objects
- Simplified file operations
- Compatible with Qt's media framework
- Automatic QFile creation

### Example

```python
from pathlib import Path
from PySide6.QtCore import QIODevice, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from winipyside.src.core.py_qiodevice import PyQFile

# Open a video file
video_path = Path("video.mp4")
file = PyQFile(video_path)
file.open(QIODevice.OpenModeFlag.ReadOnly)

# Use with QMediaPlayer
player = QMediaPlayer()
player.setAudioOutput(QAudioOutput())
player.setSourceDevice(file, QUrl.fromLocalFile(str(video_path)))
player.play()
```

## EncryptedPyQFile

Transparent AES-GCM encrypted file I/O with support for streaming and random access.

### Class Definition

```python
class EncryptedPyQFile(PyQFile):
    """Encrypted file wrapper with AES-GCM encryption."""
    
    def __init__(self, path: Path, aes_gcm: AESGCM, *args: Any, **kwargs: Any) -> None:
        """Initialize the encrypted file wrapper.
        
        Args:
            path: The file path to open.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.
        """
```

### Key Features

- **Chunked Encryption**: 64KB cipher chunks for efficient streaming
- **Random Access**: Position mapping between encrypted and decrypted data
- **Authenticated Encryption**: AES-GCM with 12-byte nonces and 16-byte tags
- **Zero-Copy Decryption**: Works seamlessly with QMediaPlayer
- **Static Methods**: Standalone encryption/decryption operations

### Encryption Constants

```python
NONCE_SIZE = 12      # 12-byte nonce for AES-GCM
TAG_SIZE = 16        # 16-byte authentication tag
CIPHER_SIZE = 64 * 1024  # 64KB cipher chunks
CHUNK_SIZE = NONCE_SIZE + CIPHER_SIZE + TAG_SIZE  # 65564 bytes total
```

### Methods

#### `readData(maxlen: int) -> bytes`

Read and decrypt data from the encrypted file.

**Parameters:**
- `maxlen` (int): Maximum number of decrypted bytes to read

**Returns:**
- `bytes`: Decrypted data

**How it works:**
1. Reads encrypted chunks from file
2. Decrypts each chunk with AES-GCM
3. Returns requested portion of decrypted data

#### `size() -> int`

Get the decrypted size of the file.

**Returns:**
- `int`: Size of decrypted data in bytes

#### `seek(pos: int) -> bool`

Seek to a position in the decrypted data.

**Parameters:**
- `pos` (int): Position in decrypted data

**Returns:**
- `bool`: True if successful

**How it works:**
1. Maps decrypted position to encrypted position
2. Seeks to start of corresponding encrypted chunk
3. Maintains offset within chunk for next read

#### Static Methods

##### `get_encrypted_pos(decrypted_pos: int) -> int`

Map a decrypted position to its corresponding encrypted position.

**Parameters:**
- `decrypted_pos` (int): Position in decrypted data

**Returns:**
- `int`: Corresponding position in encrypted data

##### `get_decrypted_pos(encrypted_pos: int) -> int`

Map an encrypted position to its corresponding decrypted position.

**Parameters:**
- `encrypted_pos` (int): Position in encrypted data

**Returns:**
- `int`: Corresponding position in decrypted data

##### `encrypt_file(input_path: Path, output_path: Path, aes_gcm: AESGCM) -> None`

Encrypt a file using AES-GCM.

**Parameters:**
- `input_path` (Path): Path to input file
- `output_path` (Path): Path to output encrypted file
- `aes_gcm` (AESGCM): AES-GCM cipher instance

**Example:**
```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winipyside.src.core.py_qiodevice import EncryptedPyQFile

# Generate key
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)

# Encrypt file
EncryptedPyQFile.encrypt_file(
    Path("video.mp4"),
    Path("video_encrypted.mp4"),
    aes_gcm
)
```

##### `decrypt_file(input_path: Path, output_path: Path, aes_gcm: AESGCM) -> None`

Decrypt a file encrypted with AES-GCM.

**Parameters:**
- `input_path` (Path): Path to encrypted file
- `output_path` (Path): Path to output decrypted file
- `aes_gcm` (AESGCM): AES-GCM cipher instance

**Example:**
```python
# Decrypt file
EncryptedPyQFile.decrypt_file(
    Path("video_encrypted.mp4"),
    Path("video_decrypted.mp4"),
    aes_gcm
)
```

### Encrypted Video Playback

The primary use case for `EncryptedPyQFile` is playing encrypted videos without creating temporary decrypted files.

**Complete Example:**

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import QUrl, QIODevice
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtMultimediaWidgets import QVideoWidget
from winipyside.src.core.py_qiodevice import EncryptedPyQFile

# Generate or load encryption key
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)

# Create application
app = QApplication([])
window = QMainWindow()
widget = QWidget()
layout = QVBoxLayout()
widget.setLayout(layout)
window.setCentralWidget(widget)

# Create video widget
video_widget = QVideoWidget()
layout.addWidget(video_widget)

# Create media player
player = QMediaPlayer()
player.setAudioOutput(QAudioOutput())
player.setVideoOutput(video_widget)

# Open encrypted file
video_path = Path("encrypted_video.mp4")
encrypted_file = EncryptedPyQFile(video_path, aes_gcm)
encrypted_file.open(QIODevice.OpenModeFlag.ReadOnly)

# Play encrypted video
player.setSourceDevice(encrypted_file, QUrl.fromLocalFile(str(video_path)))
player.play()

window.show()
app.exec()
```

## How Encryption Works

### Chunk Structure

Each encrypted chunk has the following structure:

```
[Nonce (12 bytes)][Encrypted Data (64KB)][Auth Tag (16 bytes)]
```

Total chunk size: 65,564 bytes

### Encryption Process

1. **Read plaintext chunk** (64KB)
2. **Generate random nonce** (12 bytes)
3. **Encrypt with AES-GCM** using nonce and optional AAD
4. **Write to file**: nonce + ciphertext + tag

### Decryption Process

1. **Read encrypted chunk** (65,564 bytes)
2. **Extract nonce** (first 12 bytes)
3. **Extract ciphertext + tag** (remaining bytes)
4. **Decrypt with AES-GCM** using nonce
5. **Return plaintext**

### Position Mapping

To support random access (seeking), positions must be mapped between encrypted and decrypted data:

**Decrypted → Encrypted:**
```python
chunk_index = decrypted_pos // CIPHER_SIZE
encrypted_pos = chunk_index * CHUNK_SIZE
```

**Encrypted → Decrypted:**
```python
chunk_index = encrypted_pos // CHUNK_SIZE
decrypted_pos = chunk_index * CIPHER_SIZE
```

## Best Practices

### Key Management

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Generate a new key
key = AESGCM.generate_key(bit_length=256)

# Save key securely (example - use proper key management in production)
with open("encryption.key", "wb") as f:
    f.write(key)

# Load key
with open("encryption.key", "rb") as f:
    key = f.read()
    aes_gcm = AESGCM(key)
```

### Resource Management

Always close files when done:

```python
encrypted_file = EncryptedPyQFile(path, aes_gcm)
try:
    encrypted_file.open(QIODevice.OpenModeFlag.ReadOnly)
    # Use file
    player.setSourceDevice(encrypted_file, url)
finally:
    # File will be closed when player is done
    pass
```

### Performance Considerations

- **Chunk size**: 64KB is optimized for streaming video
- **Random access**: Seeking requires reading from chunk boundaries
- **Memory usage**: Only one chunk is decrypted at a time
- **CPU usage**: AES-GCM is hardware-accelerated on modern CPUs

## See Also

- [UI Widgets - MediaPlayer](ui-widgets.md#mediaplayer) - Using encrypted files with MediaPlayer
- [Examples - Encrypted Video Player](examples.md#encrypted-video-player)
- [API Reference](api-reference.md#core-package)

