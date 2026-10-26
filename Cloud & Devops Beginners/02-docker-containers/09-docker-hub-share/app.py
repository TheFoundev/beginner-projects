#!/usr/bin/env python3
"""
Mad Libs Story Generator - Enhanced Version

Features:
  - Multiple story templates loaded from JSON
  - Word library for each story type
  - Custom word input
  - Unit tests
"""
import argparse
import json
import os
import random
import textwrap


DEFAULT_STORIES = [
    {
        "id": "adventure",
        "title": "The Great Adventure",
        "template": (
            "One day, {adjective1} {noun1} decided to go on a grand adventure to {place}. "
            "On the way, {noun1} met a {adjective2} {noun2} who was looking for a {noun3}. "
            "Together, they {verb1} through the {adjective3} forest and discovered a {noun4} "
            "that could {verb2} {number} times a day. The {noun2} was so {adjective4} that "
            "{noun1} decided to {verb3} home."
        ),
        "words": ["adjective1", "adjective2", "adjective3", "adjective4", "noun1", "noun2", "noun3",
                  "noun4", "place", "verb1", "verb2", "verb3", "number"]
    },
    {
        "id": "space",
        "title": "Space Mission",
        "template": (
            "Captain {noun1} of the spaceship {noun2} embarked on a mission to {place}. "
            "The ship was {adjective1} and carried {number} brave astronauts. "
            "They encountered a {adjective2} alien who communicated through {noun3}. "
            "The alien gifted them a {noun4} that could {verb1} and {verb2}. "
            "After {number2} days of travel, they successfully {verb3} back to Earth."
        ),
        "words": ["adjective1", "adjective2", "noun1", "noun2", "noun3", "noun4",
                  "place", "number", "number2", "verb1", "verb2", "verb3"]
    },
    {
        "id": "detective",
        "title": "The Mystery Case",
        "template": (
            "Detective {noun1} arrived at the {adjective1} mansion at {time}. "
            "The case involved a missing {noun2} and a {adjective2} butler. "
            "{noun1} deduced that the {color} {noun2} was hidden inside the {noun3}. "
            "With the help of {noun4}, the mystery was solved in {number} minutes. "
            "The culprit was {adjective3} and had been planning the theft for {number2} weeks."
        ),
        "words": ["adjective1", "adjective2", "adjective3", "color", "noun1", "noun2", "noun3",
                  "noun4", "time", "number", "number2"]
    }
]

WORD_BANK = {
    "adjective1": ["brave", "curious", "mysterious", "sparkling", "gentle", "fierce"],
    "adjective2": ["tiny", "gigantic", "mysterious", "sparkling", "fluffy", "ancient"],
    "adjective3": ["dark", "enchanted", "glowing", "whispering", "crystalline"],
    "adjective4": ["magical", "terrible", "wonderful", "splendid", "magnificent"],
    "noun1": ["dragon", "wizard", "pirate", "astronaut", "detective", "knight"],
    "noun2": ["sword", "shield", "treasure", "artifact", "book", "map"],
    "noun3": ["dragon", "monster", "genie", "phoenix", "ghost", "centaur"],
    "noun4": ["crown", "amulet", "scroll", "crystal", "key", "gem"],
    "place": ["castle", "forest", "mountain", "island", "cave", "village", "temple"],
    "verb1": ["danced", "sang", "ran", "flew", "swam", "leaped"],
    "verb2": ["100", "50", "1000", "25", "10"],
    "verb3": ["celebrated", "returned", "discovered", "defeated", "escaped"],
    "number": ["3", "7", "12", "42", "100", "5", "8"],
    "number2": ["5", "10", "3", "7", "12"],
    "color": ["red", "blue", "purple", "golden", "emerald", "silver"],
    "time": ["midnight", "noon", "dawn", "dusk", "3 AM"]
}


class MadLibsGenerator:
    """Generates Mad Libs stories from templates and word banks."""

    def __init__(self, stories=None, word_bank=None):
        self.stories = stories if stories else DEFAULT_STORIES
        self.word_bank = word_bank if word_bank else WORD_BANK

    def get_story_templates(self):
        """Return available story IDs and titles."""
        return [(s["id"], s["title"]) for s in self.stories]

    def get_story_by_id(self, story_id):
        """Get a story template by its ID."""
        return next((s for s in self.stories if s.get("id") == story_id), self.stories[0])

    def fill_template(self, story, custom_words=None):
        """Fill a story template with words."""
        custom_words = custom_words or {}
        result = {}
        for word_type in story["words"]:
            result[word_type] = custom_words.get(
                word_type, random.choice(self.word_bank.get(word_type, ["things"]))
            )
        return story["template"].format(**result)

    def generate_random(self):
        """Generate a random story."""
        story = random.choice(self.stories)
        return self.fill_template(story), story["title"]

    def generate_by_id(self, story_id, custom_words=None):
        """Generate a specific story by ID."""
        story = self.get_story_by_id(story_id)
        return self.fill_template(story, custom_words), story["title"]


def main():
    parser = argparse.ArgumentParser(
        description="A Mad Libs story generator with multiple templates.",
        epilog="""Examples:
  python app.py                        Generate a random story
  python app.py --story space          Use the Space Mission template
  python app.py --list                 List all story templates
  python app.py --interactive          Enter words manually""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--story", "-s", type=str, help="Story template ID")
    parser.add_argument("--list", action="store_true", help="List story templates")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive mode: enter words manually")
    args = parser.parse_args()

    gen = MadLibsGenerator()

    if args.list:
        print("Available story templates:")
        for story_id, title in gen.get_story_templates():
            print(f"  - {story_id}: {title}")
        return

    if args.interactive:
        print("=" * 60)
        print("  MAD LIBS - Interactive Mode")
        print("=" * 60)
        print("\nChoose a story:")
        for i, (sid, title) in enumerate(gen.get_story_templates(), 1):
            print(f"  {i}. {title} ({sid})")
        idx = int(input(f"\nEnter number (1-{len(gen.get_story_templates())}): ")) - 1
        story = gen.stories[idx]
        print(f"\nGenerating: '{story['title']}'")
        print("Leave blank for random word suggestions.\n")
        custom = {}
        prompts = {
            "adjective": "an adjective", "noun": "a noun", "place": "a place",
            "verb": "a verb (past tense)", "number": "a number",
            "color": "a color", "time": "a time of day"
        }
        for word_type in story["words"]:
            prefix = word_type.rstrip("0123456789")
            prompt = prompts.get(prefix, f"a {prefix}")
            val = input(f"  Enter {prompt}: ").strip()
            if val:
                custom[word_type] = val
        story_text, title = gen.generate_by_id(story["id"], custom)
        print("\n" + "=" * 60)
        print(f"  YOUR STORY: {title}")
        print("=" * 60)
        print(textwrap.fill(story_text, width=60))
        return

    if args.story:
        story_text, title = gen.generate_by_id(args.story)
    else:
        story_text, title = gen.generate_random()

    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    print(textwrap.fill(story_text, width=60))
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
