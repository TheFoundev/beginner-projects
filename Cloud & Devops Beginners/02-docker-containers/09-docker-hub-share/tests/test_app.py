"""
Tests for the MadLibsGenerator class.
Run: python -m pytest tests/ -v
"""
import pytest
import sys
import os
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import MadLibsGenerator


@pytest.fixture
def generator():
    return MadLibsGenerator()


class TestMadLibsGenerator:

    def test_default_stories_loaded(self, generator):
        assert len(generator.stories) >= 3

    def test_word_bank_has_entries(self, generator):
        assert len(generator.word_bank) >= 10

    def test_get_story_templates(self, generator):
        templates = generator.get_story_templates()
        assert ("adventure", "The Great Adventure") in templates
        assert ("space", "Space Mission") in templates
        assert ("detective", "The Mystery Case") in templates

    def test_get_story_by_id(self, generator):
        story = generator.get_story_by_id("space")
        assert story["title"] == "Space Mission"

    def test_get_story_by_invalid_id(self, generator):
        story = generator.get_story_by_id("nonexistent")
        assert story["id"] == "adventure"

    def test_generate_random(self, generator):
        story_text, title = generator.generate_random()
        assert isinstance(story_text, str)
        assert len(story_text) > 50
        assert title in ["The Great Adventure", "Space Mission", "The Mystery Case"]

    def test_generate_by_id(self, generator):
        story_text, title = generator.generate_by_id("detective")
        assert title == "The Mystery Case"
        assert "{noun1}" not in story_text

    def test_fill_template_with_custom_words(self, generator):
        story = generator.stories[0]
        custom = {"noun1": "Superman", "place": "Metropolis"}
        text = generator.fill_template(story, custom)
        assert "Superman" in text
        assert "Metropolis" in text

    def test_fill_template_random_words(self, generator):
        story = generator.stories[0]
        text = generator.fill_template(story)
        assert "{adjective1}" not in text
        assert "{noun1}" not in text

    def test_template_placeholders_all_replaced(self, generator):
        for story in generator.stories:
            text = generator.fill_template(story)
            assert "{" not in text, f"Unfilled placeholder in {story['title']}"

    def test_all_stories_have_word_lists(self, generator):
        for story in generator.stories:
            assert "words" in story
            assert "template" in story
            assert "title" in story
            assert len(story["words"]) >= 10
