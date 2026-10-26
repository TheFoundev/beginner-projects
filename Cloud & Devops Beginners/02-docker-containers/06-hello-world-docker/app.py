"""
Docker Hello World - Enhanced Version

A greeting application that supports multiple languages and command-line arguments.
This demonstrates environment variable configuration and user interaction in Docker.
"""
import argparse
import os
from datetime import datetime


class GreetingGenerator:
    """Generates personalized greetings in multiple languages."""

    GREETINGS = {
        "english": "Hello",
        "spanish": "Hola",
        "french": "Bonjour",
        "german": "Hallo",
        "japanese": "Konnichiwa",
        "italian": "Ciao",
        "portuguese": "Ola",
        "russian": "Privet",
    }

    def __init__(self):
        self.name = os.environ.get("GREETING_NAME", "Docker")
        self.language = os.environ.get("GREETING_LANG", "english").lower()
        self.greeting_count = 0

    def greet(self, name=None, language=None):
        """Generate a greeting message."""
        name = name or self.name
        language = language or self.language

        greeting = self.GREETINGS.get(language, self.GREETINGS["english"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.greeting_count += 1

        return (
            f"{'=' * 50}\n"
            f"  {greeting}, {name}!\n"
            f"{'=' * 50}\n"
            f"  Language: {language.capitalize()}\n"
            f"  Timestamp: {timestamp}\n"
            f"  Greetings served: {self.greeting_count}\n"
            f"  Container: {os.uname().nodename if hasattr(os, 'uname') else 'N/A'}\n"
            f"{'=' * 50}"
        )

    def list_languages(self):
        """List all available languages."""
        return list(self.GREETINGS.keys())


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="A multilingual greeting application running in Docker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python app.py                    Greet the default name
  python app.py --name Alice       Greet Alice
  python app.py --lang spanish     Greet in Spanish
  python app.py --name Bob --lang japanese
  python app.py --list             List all available languages
Environment Variables:
  GREETING_NAME  Default name to greet (default: Docker)
  GREETING_LANG  Default language (default: english)
        """
    )

    parser.add_argument("--name", "-n", type=str, help="Name to greet")
    parser.add_argument("--lang", "-l", type=str, help="Language for greeting")
    parser.add_argument("--list", action="store_true", help="List available languages")

    args = parser.parse_args()

    generator = GreetingGenerator()

    if args.list:
        langs = generator.list_languages()
        print("Available languages:")
        for lang in langs:
            marker = " ←" if lang == generator.language else ""
            print(f"  - {lang}{marker}")
        return

    print(generator.greet(args.name, args.lang))


if __name__ == "__main__":
    main()
