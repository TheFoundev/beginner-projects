"""
Tests for app.py — GreetingGenerator class
Uses pytest for structured testing inside Docker.
Run: python -m pytest tests/ -v
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import GreetingGenerator


@pytest.fixture
def generator():
    """Create a greeting generator instance."""
    return GreetingGenerator()


class TestGreetingGenerator:

    def test_default_name(self, generator):
        """Test that the default name is 'Docker'."""
        assert generator.name == "Docker"

    def test_default_language(self, generator):
        """Test that the default language is English."""
        assert generator.language == "english"

    def test_greet_english(self, generator):
        """Test English greeting."""
        result = generator.greet("Alice", "english")
        assert "Hello, Alice!" in result

    def test_greet_spanish(self, generator):
        """Test Spanish greeting."""
        result = generator.greet("Bob", "spanish")
        assert "Hola, Bob!" in result

    def test_greet_japanese(self, generator):
        """Test Japanese greeting."""
        result = generator.greet("Yuki", "japanese")
        assert "Konnichiwa, Yuki!" in result

    def test_greet_default_language(self, generator):
        """Test using default language when none specified."""
        result = generator.greet("Charlie")
        assert "Hello, Charlie!" in result

    def test_greeting_count(self, generator):
        """Test that greeting count increments."""
        assert generator.greeting_count == 0
        generator.greet("Alice")
        assert generator.greeting_count == 1
        generator.greet("Bob")
        assert generator.greeting_count == 2

    def test_list_languages(self, generator):
        """Test listing all available languages."""
        langs = generator.list_languages()
        assert "english" in langs
        assert "spanish" in langs
        assert "japanese" in langs
        assert len(langs) >= 5

    def test_unknown_language_falls_back(self, generator):
        """Test that unknown languages fall back to English."""
        result = generator.greet("Test", "klingon")
        assert "Hello, Test!" in result

    def test_environment_variable_name(self, generator, monkeypatch):
        """Test that name can be set via environment variable."""
        monkeypatch.setenv("GREETING_NAME", "Environment")
        gen = GreetingGenerator()
        assert gen.name == "Environment"

    def test_environment_variable_language(self, monkeypatch):
        """Test that language can be set via environment variable."""
        monkeypatch.setenv("GREETING_LANG", "french")
        gen = GreetingGenerator()
        assert gen.language == "french"
