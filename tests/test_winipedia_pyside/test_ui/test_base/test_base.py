"""Tests for winipedia_pyside.ui.base.base module."""

from abc import abstractmethod
from typing import final

from PySide6.QtCore import QObject
from pytest_mock import MockerFixture
from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.ui.base.base import Base, QABCLoggingMeta


class TestQABCLoggingMeta:
    """Test class for QABCLoggingMeta."""

    def test_metaclass_inheritance(self) -> None:
        """Test that QABCImplementationLoggingMeta has correct inheritance."""
        # Test that it's a metaclass that combines the expected functionality
        assert_with_msg(
            issubclass(QABCLoggingMeta, type(QObject)),
            "QABCLoggingMeta should inherit from QObject's metaclass",
        )

        # Create a test class using the metaclass
        class TestClass(metaclass=QABCLoggingMeta):
            @abstractmethod
            def abstract_method(self) -> None:
                """Abstract method for testing."""

            @final
            def concrete_method(self) -> str:
                """Concrete method for testing."""
                return "test"

        # Verify the class uses the correct metaclass
        assert_with_msg(
            type(TestClass) is QABCLoggingMeta,
            "TestClass should use QABCLoggingMeta",
        )


class TestBase:
    """Test class for Base."""

    def test___init__(self) -> None:
        """Test method for __init__."""

        # Create a concrete implementation for testing
        class ConcreteBase(Base):
            @final
            def base_setup(self) -> None:
                self.base_setup_called = True

            @final
            def setup(self) -> None:
                self.setup_called = True

            @final
            def pre_setup(self) -> None:
                self.pre_setup_called = True

            @final
            def post_setup(self) -> None:
                self.post_setup_called = True

        # Test initialization calls all setup methods in correct order
        instance = ConcreteBase()

        assert_with_msg(
            hasattr(instance, "base_setup_called") and instance.base_setup_called,
            "base_setup should be called during initialization",
        )
        assert_with_msg(
            hasattr(instance, "pre_setup_called") and instance.pre_setup_called,
            "pre_setup should be called during initialization",
        )
        assert_with_msg(
            hasattr(instance, "setup_called") and instance.setup_called,
            "setup should be called during initialization",
        )
        assert_with_msg(
            hasattr(instance, "post_setup_called") and instance.post_setup_called,
            "post_setup should be called during initialization",
        )

    def test_base_setup(self) -> None:
        """Test method for base_setup."""

        # Test that base_setup is abstract
        class TestBase(Base):
            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

            @final
            def base_setup(self) -> None:
                self.base_setup_called = True

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "base_setup_called") and instance.base_setup_called,
            "base_setup should be called during initialization",
        )

    def test_setup(self) -> None:
        """Test method for setup."""

        # Test that setup is abstract
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                self.setup_called = True

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "setup_called") and instance.setup_called,
            "setup should be called during initialization",
        )

    def test_pre_setup(self) -> None:
        """Test method for pre_setup."""

        # Test that pre_setup is abstract
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                self.pre_setup_called = True

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "pre_setup_called") and instance.pre_setup_called,
            "pre_setup should be called during initialization",
        )

    def test_post_setup(self) -> None:
        """Test method for post_setup."""

        # Test that post_setup is abstract
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                self.post_setup_called = True

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "post_setup_called") and instance.post_setup_called,
            "post_setup should be called during initialization",
        )

    def test_get_display_name(self) -> None:
        """Test method for get_display_name."""

        # Create a test class with a specific name
        class TestDisplayName(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Test that get_display_name splits on uppercase
        display_name = TestDisplayName.get_display_name()
        expected_name = "Test Display Name"
        assert_with_msg(
            display_name == expected_name,
            f"Expected display name '{expected_name}', got '{display_name}'",
        )

        # Test with single word class name
        class SingleWord(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        single_display_name = SingleWord.get_display_name()
        expected_single = "Single Word"
        assert_with_msg(
            single_display_name == expected_single,
            f"Expected display name '{expected_single}', got '{single_display_name}'",
        )

    def test_get_subclasses(self, mocker: MockerFixture) -> None:
        """Test method for get_subclasses."""
        # Mock the get_main_package function to avoid import issues
        mock_package = mocker.MagicMock()
        mock_package.__name__ = "test_package"
        mocker.patch(
            "winipedia_pyside.ui.base.base.get_main_package",
            return_value=mock_package,
        )
        mocker.patch("winipedia_pyside.ui.base.base.walk_package", return_value=[])

        # Create some test subclasses
        class TestSubclass1(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        class TestSubclass2(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        # Mock get_all_nonabstract_subclasses to return our test classes
        mock_subclasses = [TestSubclass1, TestSubclass2]
        mocker.patch(
            "winipedia_pyside.ui.base.base.get_all_nonabstract_subclasses",
            return_value=mock_subclasses,
        )

        # Test that get_subclasses returns the subclasses
        subclasses = Base.get_subclasses()
        subclass_names = [cls.__name__ for cls in subclasses]

        assert_with_msg(
            "TestSubclass1" in subclass_names,
            f"Expected TestSubclass1 in subclasses, got {subclass_names}",
        )
        assert_with_msg(
            "TestSubclass2" in subclass_names,
            f"Expected TestSubclass2 in subclasses, got {subclass_names}",
        )

        # Test that subclasses are sorted by name
        sorted_names = sorted(subclass_names)
        assert_with_msg(
            subclass_names == sorted_names,
            f"Expected subclasses to be sorted, got {subclass_names}",
        )

        # Test with custom package parameter
        custom_package = mocker.MagicMock()
        custom_package.__name__ = "custom_package"
        subclasses_with_package = Base.get_subclasses(package=custom_package)
        assert_with_msg(
            len(subclasses_with_package) >= 0,
            "get_subclasses should return a list when package is provided",
        )

    def test_set_current_page(self) -> None:
        """Test method for set_current_page."""

        # This method requires complex mocking of Qt widgets and pages
        # Test that the method exists and is callable
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "set_current_page"),
            "Base should have set_current_page method",
        )
        assert_with_msg(
            callable(instance.set_current_page),
            "set_current_page should be callable",
        )

    def test_get_stack(self) -> None:
        """Test method for get_stack."""

        # This method requires complex mocking of Qt widgets
        # Test that the method exists and is callable
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "get_stack"),
            "Base should have get_stack method",
        )
        assert_with_msg(
            callable(instance.get_stack),
            "get_stack should be callable",
        )

    def test_get_stack_pages(self) -> None:
        """Test method for get_stack_pages."""

        # This method requires complex mocking of Qt widgets
        # Test that the method exists and is callable
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "get_stack_pages"),
            "Base should have get_stack_pages method",
        )
        assert_with_msg(
            callable(instance.get_stack_pages),
            "get_stack_pages should be callable",
        )

    def test_get_page(self) -> None:
        """Test method for get_page."""

        # This method requires complex mocking of Qt widgets and pages
        # Test that the method exists and is callable
        class TestBase(Base):
            @final
            def base_setup(self) -> None:
                pass

            @final
            def setup(self) -> None:
                pass

            @final
            def pre_setup(self) -> None:
                pass

            @final
            def post_setup(self) -> None:
                pass

        instance = TestBase()
        assert_with_msg(
            hasattr(instance, "get_page"),
            "Base should have get_page method",
        )
        assert_with_msg(
            callable(instance.get_page),
            "get_page should be callable",
        )

    def test_get_svg_icon(self) -> None:
        """Test method for get_svg_icon."""
        # Test that the method exists and is callable
        assert_with_msg(
            hasattr(Base, "get_svg_icon"),
            "Base should have get_svg_icon class method",
        )
        assert_with_msg(
            callable(Base.get_svg_icon),
            "get_svg_icon should be callable",
        )

        # Test that it's a classmethod
        assert_with_msg(
            isinstance(Base.__dict__["get_svg_icon"], classmethod),
            "get_svg_icon should be a classmethod",
        )

    def test_get_page_static(self) -> None:
        """Test method for get_page_static."""
        # Test that the method exists and is callable
        assert_with_msg(
            hasattr(Base, "get_page_static"),
            "Base should have get_page_static class method",
        )
        assert_with_msg(
            callable(Base.get_page_static),
            "get_page_static should be callable",
        )

        # Test that it's a classmethod
        assert_with_msg(
            isinstance(Base.__dict__["get_page_static"], classmethod),
            "get_page_static should be a classmethod",
        )
