import random

def load_quotes():
    """Load quotes from the quotes.txt file."""
    try:
        with open("quotes.txt", "r") as file:
            quotes = [line.strip() for line in file if line.strip()]
        return quotes
    except FileNotFoundError:
        return ["You can do great things! - Keep believing!"]

def get_random_quote(quotes):
    """Return a random quote from the list."""
    return random.choice(quotes)

def main():
    """Main interactive quote generator."""
    print("=" * 50)
    print("  M O T I V A T I O N A L   Q U O T E   G E N")
    print("  (running inside a Docker container)")
    print("=" * 50)
    print()

    quotes = load_quotes()

    while True:
        user_input = input("Press Enter to get a motivational quote, or type 'q' to quit: ")
        if user_input.lower() == 'q':
            print("\nThanks for stopping by! Stay motivated. 💪")
            break
        print()
        print(get_random_quote(quotes))
        print()

if __name__ == "__main__":
    main()
