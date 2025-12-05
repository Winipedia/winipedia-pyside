# Winipyside Documentation

Welcome to the comprehensive documentation for **Winipyside**, a PySide6 utilities package for building modern Qt desktop applications.

## Table of Contents

### Core Documentation

- **[Core Package](core.md)** - Encrypted file I/O and QIODevice wrappers
  - PyQIODevice - Python-friendly QIODevice wrapper
  - PyQFile - File operations with Path support
  - EncryptedPyQFile - Transparent AES-GCM encryption

### UI Framework Documentation

- **[UI Base](ui-base.md)** - Foundation framework and lifecycle management
  - Base class with lifecycle hooks
  - QABCLoggingMeta metaclass
  - Navigation and utility methods

- **[UI Widgets](ui-widgets.md)** - Reusable widgets
  - Notification - Toast notifications
  - Browser - Embedded web browser with cookie management
  - MediaPlayer - Full-featured media player
  - ClickableWidget - Click-enabled widgets

- **[UI Pages](ui-pages.md)** - Page components for navigation
  - Base page class
  - Player page
  - Browser page

- **[UI Windows](ui-windows.md)** - Main window framework
  - Base window class
  - Page management
  - Navigation system

### Additional Resources

- **[API Reference](api-reference.md)** - Complete API documentation
- **[Examples](examples.md)** - Code examples and tutorials
- **[Best Practices](best-practices.md)** - Design patterns and recommendations

## Quick Links

### Getting Started

1. [Installation](../README.md#installation)
2. [Quick Start](../README.md#quick-start)
3. [Basic Application Example](examples.md#basic-application)

### Common Use Cases

- [Playing Encrypted Videos](core.md#encrypted-video-playback)
- [Building Multi-Page Applications](ui-windows.md#multi-page-application)
- [Cookie Management in Browser](ui-widgets.md#browser-cookie-management)
- [Custom Lifecycle Hooks](ui-base.md#lifecycle-hooks)

## Architecture Overview

Winipyside is organized into several key packages:

```
winipyside/src/
├── core/              # Low-level I/O and encryption
│   └── py_qiodevice.py
└── ui/                # UI framework and components
    ├── base/          # Foundation classes
    ├── widgets/       # Reusable widgets
    ├── pages/         # Page components
    └── windows/       # Window framework
```

### Design Philosophy

1. **Type Safety**: 100% type annotated with strict mypy checking
2. **Modularity**: Reusable components with clear interfaces
3. **Lifecycle Management**: Consistent initialization patterns
4. **Testability**: Designed for easy testing with pytest-qt
5. **Production Ready**: CI/CD workflows for headless environments

## Key Concepts

### Lifecycle Hooks

All UI components follow a 4-phase initialization pattern:

1. **`base_setup()`** - Initialize Qt components
2. **`pre_setup()`** - Setup before main initialization
3. **`setup()`** - Main setup logic
4. **`post_setup()`** - Finalization after setup

### Page-Based Navigation

Applications use a QStackedWidget-based navigation system:

- **Windows** contain multiple **Pages**
- **Pages** can navigate to other pages
- Automatic menu generation for page switching

### Encrypted I/O

Transparent encryption/decryption using AES-GCM:

- Chunked encryption for efficient streaming
- Position mapping for random access
- Zero-copy decryption for media playback

## Contributing

See the [Contributing Guide](../README.md#contributing) for information on:

- Setting up the development environment
- Running tests
- Code quality standards
- Submitting pull requests

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Winipedia/winipyside/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/Winipedia/winipyside/discussions)
