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
        primarySwatch: Colors.purple,
        brightness: Brightness.light,
      ),
      home: const QuoteGeneratorHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class Quote {
  final String text;
  final String author;

  Quote({required this.text, required this.author});
}

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
  bool _showPunchline = false;

  void _generateNewQuote() {
    setState(() {
      int newIndex;
      do {
        newIndex = _random.nextInt(quotes.length);
      } while (newIndex == _currentIndex);
      _currentIndex = newIndex;
      _showPunchline = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final quote = quotes[_currentIndex];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Daily Quote Generator'),
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.purple[50]!,
              Colors.deepPurple[50]!,
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.format_quote,
                size: 60,
                color: Colors.deepPurple,
              ),
              const SizedBox(height: 20),
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
                  margin: const EdgeInsets.symmetric(horizontal: 24),
                  child: Padding(
                    padding: const EdgeInsets.all(32),
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
              const SizedBox(height: 30),
              Text(
                "${_currentIndex + 1} of ${quotes.length} quotes",
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: 200,
                child: ElevatedButton.icon(
                  onPressed: _generateNewQuote,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
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
    );
  }
}
