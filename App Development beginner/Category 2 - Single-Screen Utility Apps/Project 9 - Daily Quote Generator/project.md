# Project 9 - Daily Quote Generator (Flutter)

## 1. Project Title
**Daily Quote Generator**

## 2. The Concept
This app displays a random inspirational quote each time you tap the "New Quote" button. Think of it as a digital fortune cookie — you crack it open (tap the button), and a new piece of wisdom appears on the screen. Behind the scenes, the app has a list of pre-saved quotes (like a deck of quote cards), and each tap shuffles the deck and picks one card at random to show you.

## 3. What You Will Build/Do
You'll build a beautiful app with a quote displayed in an elegant card, an author name below it, and a "New Quote" button at the bottom. Each tap reveals a new motivational message with a smooth fade animation. The final app looks like a polished quote journal — perfect for starting your day with inspiration.

## 4. Core App Concept
**List Indexing and Random Selection** — The app stores a collection of items (quotes) in a list, picks one at random using a random number, and displays it. Like a raffle drum: all the tickets (quotes) are inside, the drum spins, and one ticket (quote) gets pulled out to win.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone

## 6. What You Will Learn
- Managing a local list of data (quotes)
- Random selection from a list with proper indexing
- Adding smooth animations for visual polish
- Building a clean, card-based UI design

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create quote_generator
cd quote_generator
```

### Step 2: Add Dependencies (optional for clipboard)
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  font_awesome_flutter: ^10.7.0
```

### Step 3: Complete Source Code

```dart
import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const QuoteGeneratorApp());
}

class QuoteGeneratorApp extends StatelessWidget {
  const QuoteGeneratorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Daily Quote Generator',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        brightness: Brightness.light,
        useMaterial3: true,
      ),
      home: const QuoteGeneratorHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// Quote data model
class Quote {
  final String text;
  final String author;

  Quote({
    required this.text,
    required this.author,
  });
}

// List of inspirational quotes
final List<Quote> quotes = [
  Quote(
    text: "The only way to do great work is to love what you do.",
    author: "Steve Jobs",
  ),
  Quote(
    text: "Life is what happens when you're busy making other plans.",
    author: "John Lennon",
  ),
  Quote(
    text: "The future belongs to those who believe in the beauty of their dreams.",
    author: "Eleanor Roosevelt",
  ),
  Quote(
    text: "Don't watch the clock; do what it does. Keep going.",
    author: "Sam Levenson",
  ),
  Quote(
    text: "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    author: "Winston Churchill",
  ),
  Quote(
    text: "The only impossible journey is the one you never begin.",
    author: "Mark Twain",
  ),
  Quote(
    text: "In the middle of every difficulty lies opportunity.",
    author: "Albert Einstein",
  ),
  Quote(
    text: "You are never too old to set another goal or to dream a new dream.",
    author: "Maya Angelou",
  ),
  Quote(
    text: "The journey of a thousand miles begins with one step.",
    author: "Lao Tzu",
  ),
  Quote(
    text: "Believe you can and you're halfway there.",
    author: "Theodore Roosevelt",
  ),
  Quote(
    text: "Your time is limited, don't waste it living someone else's life.",
    author: "Steve Jobs",
  ),
  Quote(
    text: "The best time to plant a tree was 20 years ago. The second best time is now.",
    author: "Chinese Proverb",
  ),
  Quote(
    text: "Every strike brings me closer to the next home run.",
    author: "Babe Ruth",
  ),
  Quote(
    text: "The harder the conflict, the greater the triumph.",
    author: "Thomas Fuller",
  ),
  Quote(
    text: "Creativity is intelligence having fun.",
    author: "Albert Einstein",
  ),
];

class QuoteGeneratorHome extends StatefulWidget {
  const QuoteGeneratorHome({super.key});

  @override
  State<QuoteGeneratorHome> createState() => _QuoteGeneratorHomeState();
}

class _QuoteGeneratorHomeState extends State<QuoteGeneratorHome> {
  final Random _random = Random();
  int _currentIndex = 0;
  bool _isAnimating = false;

  void _generateNewQuote() {
    setState(() {
      if (_isAnimating) return;
      _isAnimating = true;
      
      // Generate a new index that's different from the current one
      int newIndex;
      do {
        newIndex = _random.nextInt(quotes.length);
      } while (newIndex == _currentIndex);
      
      _currentIndex = newIndex;
      _isAnimating = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final quote = quotes[_currentIndex];

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.deepPurple[50]!,
              Colors.purple[50]!,
              Colors.deepOrange[50]!,
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Quote icon
                const Icon(
                  Icons.format_quote,
                  size: 60,
                  color: Colors.deepPurple,
                ),
                const SizedBox(height: 20),
                
                // Quote card with animated fade
                AnimatedSwitcher(
                  duration: const Duration(milliseconds: 500),
                  transitionBuilder: (Widget child, Animation<double> animation) {
                    return FadeTransition(
                      opacity: animation,
                      child: ScaleTransition(
                        scale: Tween<double>(begin: 0.9, end: 1.0).animate(
                          CurvedAnimation(parent: animation, curve: Curves.easeOutBack),
                        ),
                        child: child,
                      ),
                    );
                  },
                  child: Card(
                    key: ValueKey<int>(_currentIndex),
                    elevation: 8,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(28),
                      child: Column(
                        children: [
                          Text(
                            quote.text,
                            style: const TextStyle(
                              fontSize: 22,
                              fontStyle: FontStyle.italic,
                              height: 1.4,
                              color: Colors.black87,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 20),
                          Text(
                            "— ${quote.author}",
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Colors.deepPurple[700],
                            ),
                            textAlign: TextAlign.right,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                
                const SizedBox(height: 20),
                
                // Quote counter
                Text(
                  "${_currentIndex + 1} of ${quotes.length} quotes",
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
                
                const SizedBox(height: 24),
                
                // New quote button
                SizedBox(
                  width: 200,
                  child: ElevatedButton.icon(
                    onPressed: _generateNewQuote,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.deepPurple,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 24,
                        vertical: 16,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                    ),
                    icon: const Icon(Icons.refresh),
                    label: const Text(
                      'New Quote',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

### Step 4: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add categories (motivational, funny, wisdom, etc.)
- Add a "favorite quotes" feature with local storage
- Add share functionality to share quotes on social media
- Add a dark mode toggle
- Add daily notification with a quote
