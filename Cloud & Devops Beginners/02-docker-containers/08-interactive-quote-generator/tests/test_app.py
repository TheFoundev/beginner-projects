"""
Tests for the Quote Generator.
Run: python -m pytest tests/ -v
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import QuoteGenerator


@pytest.fixture
def generator():
    """Create a quote generator with default quotes."""
    return QuoteGenerator()


@pytest.fixture
def generator_with_file(tmp_path):
    """Create a generator using a temporary quotes file."""
    import json
    quotes_data = [
        {"text": "Test quote 1", "author": "Tester", "category": "test"},
        {"text": "Test quote 2", "author": "Tester", "category": "demo"},
    ]
    quotes_file = tmp_path / "quotes.json"
    quotes_file.write_text(json.dumps(quotes_data))
    return QuoteGenerator(str(quotes_file))


class TestQuoteGenerator:

    def test_default_quotes_loaded(self, generator):
        """Ensure default quotes load correctly."""
        assert len(generator.quotes) > 0
        assert len(generator.quotes) >= 5

    def test_load_from_file(self, generator_with_file):
        """Ensure quotes can be loaded from a JSON file."""
        assert len(generator_with_file.quotes) == 2

    def test_get_categories(self, generator):
        """Ensure categories are extracted from quotes."""
        cats = generator.get_categories()
        assert "motivation" in cats
        assert "wisdom" in cats
        assert len(cats) >= 3

    def test_random_quote_returns_dict(self, generator):
        """Ensure a quote is returned as a dict with 'text' key."""
        quote = generator.get_random_quote()
        assert "text" in quote
        assert "author" in quote

    def test_random_quote_with_category(self, generator):
        """Ensure filtering by category works."""
        quote = generator.get_random_quote("wisdom")
        assert quote.get("category") == "wisdom"

    def test_random_quote_with_nonexistent_category(self, generator):
        """Ensure fallback to all quotes when category doesn't exist."""
        quote = generator.get_random_quote("nonexistent-category")
        assert "text" in quote

    def test_count_by_category(self, generator):
        """Ensure category counts are correct."""
        counts = generator.count_by_category()
        assert sum(counts.values()) == len(generator.quotes)

    def test_history_tracking(self, generator):
        """Ensure quotes are tracked in history."""
        initial_len = len(generator.history)
        generator.get_random_quote()
        assert len(generator.history) == initial_len + 1

    def test_format_quote(self, generator):
        """Ensure quote formatting includes the text."""
        quote = generator.get_random_quote()
        formatted = generator.format_quote(quote)
        assert quote["text"] in formatted
        assert "──" in formatted

    def test_all_quotes_count(self, generator):
        """Ensure get_all_quotes returns all quotes."""
        all_quotes = generator.get_all_quotes()
        assert len(all_quotes) == len(generator.quotes)
